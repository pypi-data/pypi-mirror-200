import re
import json
import os
from typing import Optional
from dataclasses import dataclass
from io import BytesIO

import exiftool
from quart_kroket.data.checksum import md5_string
from quart_kroket.media import proportional_scale
from slugify import slugify
from wfs.db.utils import ts_vectorize
from quart_kroket.data.checksum import md5_string


import magic
import mutagen
import ffmpeg


@dataclass
class MediaMusicMeta:
    path: str
    duration: float
    mime: str
    size: int
    bitrate: int
    channels: int
    sample_rate: int
    artist: Optional[str]
    title: Optional[str]

    @classmethod
    def from_path(cls, path) -> 'MediaMusicMeta':
        metadata = mutagen.File(path)
        mime = metadata.mime[0]

        try:
            duration = metadata.info.length
        except:
            duration = 0

        artist = metadata.tags.get('artist')
        if artist:
            artist = artist[0]
        title = metadata.tags.get('title')
        if title:
            title = title[0]

        if not artist or not title:
            # try .info.json
            path_info = f"{path}.info.json"
            if os.path.exists(path_info):
                try:
                    blob = json.load(open(path_info,))
                    artist = blob.get('artist')
                    title = blob.get('title')
                    duration = blob.get('duration', 0)
                except:
                    pass
            else:
                artist = 'Unknown'
                title = 'Unknown'

        bitrate = metadata.info.bitrate
        channels = metadata.info.channels
        sample_rate = metadata.info.sample_rate

        return MediaMusicMeta(
            path=path,
            mime=mime,
            size=os.path.getsize(path),
            bitrate=bitrate,
            channels=channels,
            sample_rate=sample_rate,
            duration=duration,
            artist=artist,
            title=title
        )


@dataclass
class MediaImageMeta:
    path: str
    width: int
    height: int
    size: int
    mimetype: str

    async def generate_thumbnail(self, path_out) -> 'MediaImageMeta':
        from quart_kroket.imaging.imaging import image_sanitize_resize
        res = await image_sanitize_resize(
            buffer_or_path=self.path,
            path_out=path_out,
            extension="jpeg",
            min_size=48,
            max_size=512,
            quality=50)

        mimetype = magic.from_file(res.path, mime=True)
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(res.path)
            dimensions = metadata[0]['Composite:ImageSize'].split(" ", 1)
            dimensions = list(map(int, dimensions))

        return MediaImageMeta(
            path=res.path,
            mimetype=mimetype,
            width=dimensions[0],
            height=dimensions[1],
            size=os.path.getsize(res.path))

    @classmethod
    def from_path(cls, path) -> 'MediaImageMeta':
        mimetype = magic.from_file(path, mime=True)

        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(path)
            dimensions = metadata[0]['Composite:ImageSize'].split(" ", 1)
            dimensions = list(map(int, dimensions))

        return cls(path=path,
                   mimetype=mimetype,
                   width=dimensions[0],
                   height=dimensions[1],
                   size=os.path.getsize(path))

    @property
    def ext(self):
        return self.mimetype.split("/")[1]


@dataclass
class MediaVideoMeta:
    path: str
    width: int
    height: int
    duration: float
    mime: str
    fps: float
    codec: str
    size: int

    @classmethod
    def from_path(cls, path) -> 'MediaVideoMeta':
        video_stream = ffmpeg.probe(path, select_streams="v")
        stream0 = next(v for v in video_stream['streams'] if v['codec_type'] == 'video')
        duration = float(stream0['duration'])
        if 'r_frame_rate' in stream0:
            avg_frame_rate = stream0['r_frame_rate']
        else:
            avg_frame_rate = stream0['avg_frame_rate']

        codec = stream0['codec_name']
        if "/" in avg_frame_rate:
            avg_frame_rate = int(avg_frame_rate.split("/")[0])
        else:
            avg_frame_rate = int(avg_frame_rate)

        if 1000 <= avg_frame_rate <= 30000:
            avg_frame_rate = int(avg_frame_rate / 1000)
        if avg_frame_rate > 30:
            avg_frame_rate = 30

        return cls(
            path=path,
            mime=magic.from_file(path, mime=True),
            codec=codec,
            size=os.path.getsize(path),
            width=stream0['width'],
            height=stream0['height'],
            fps=avg_frame_rate,
            duration=duration)

    async def generate_preview(self, path_out, max_width_or_height=512, **kwargs) -> 'MediaAnimatedMeta':
        from quart_kroket.imaging.imaging import image_sanitize_resize, thumbnail_video, web_video, SubprocessResult

        width, height = proportional_scale(
            width=self.width, height=self.height,
            max_width_or_height=max_width_or_height)

        kwargs["fps"] = kwargs.get("fps", 10)
        kwargs["duration"] = kwargs.get("duration", 4)
        kwargs["quality"] = kwargs.get("quality", 30)
        kwargs["ffmpeg_ss"] = kwargs.get("ffmpeg_ss")

        res: SubprocessResult = await web_video(
            path_input=self.path,
            path_output=path_out,
            video_type="webm",
            width=width,
            height=height,
            **kwargs
        )
        return MediaAnimatedMeta.from_path(res.extra)

    async def generate_thumbnail(self, path_out, max_width_or_height: int = 512, **kwargs) -> 'MediaImageMeta':
        from quart_kroket.imaging.imaging import thumbnail_video, SubprocessResult

        kwargs["ffmpeg_ss"] = kwargs.get("ffmpeg_ss", int(self.duration / 2))

        width, height = proportional_scale(
            width=self.width, height=self.height,
            max_width_or_height=max_width_or_height)

        res: SubprocessResult = await thumbnail_video(
            path_input=self.path,
            path_output=path_out,
            width=width,
            height=height,
            **kwargs
        )
        return MediaImageMeta.from_path(res.extra)


@dataclass
class MediaAnimatedMeta:
    path: str
    width: int
    height: int
    duration: float
    fps: int
    mime: str
    codec: str
    size: int

    @property
    def is_gif(self):
        return self.mime == "image/gif"

    @property
    def is_animated(self):
        return self.mime == "image/webp"

    @classmethod
    def from_path(cls, path) -> 'MediaAnimatedMeta':
        if path.lower().endswith(".gif"):
            video_stream = ffmpeg.probe(path, select_streams="v")
            stream0 = next(v for v in video_stream['streams'] if v['codec_type'] == 'video')
            duration = float(stream0['duration'])
            avg_frame_rate = stream0['avg_frame_rate']
            codec = stream0['codec_name']
            if "/" in avg_frame_rate:
                avg_frame_rate = int(avg_frame_rate.split("/")[0])
            else:
                avg_frame_rate = int(avg_frame_rate)

            if 1000 <= avg_frame_rate <= 30000:
                avg_frame_rate = int(avg_frame_rate/1000)
            if avg_frame_rate > 30:
                avg_frame_rate = 30

            return cls(
                path=path,
                mime='image/gif',
                codec=codec,
                size=os.path.getsize(path),
                width=stream0['width'],
                height=stream0['height'],
                fps=avg_frame_rate,
                duration=duration)

        elif path.lower().endswith(".webm"):
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(path)
                dimensions = metadata[0]['Composite:ImageSize'].split(" ", 1)
                dimensions = list(map(int, dimensions))
                duration = metadata[0]['Matroska:Duration']
                mimetype = metadata[0]['File:MIMEType']

                return cls(
                    path=path,
                    mime=mimetype,
                    codec='webm',
                    size=os.path.getsize(path),
                    width=dimensions[0],
                    height=dimensions[1],
                    fps=0,
                    duration=duration)
        else:
            raise Exception("unknown filetype")

    async def generate_preview(self, path_out, max_width_or_height=512, **kwargs) -> 'MediaAnimatedMeta':
        from quart_kroket.imaging.imaging import image_sanitize_resize, thumbnail_video, web_video, SubprocessResult

        width, height = proportional_scale(
            width=self.width, height=self.height,
            max_width_or_height=max_width_or_height)

        kwargs["fps"] = kwargs.get("fps", 10)
        kwargs["duration"] = kwargs.get("duration", 4)
        kwargs["quality"] = kwargs.get("quality", 30)
        kwargs["ffmpeg_ss"] = kwargs.get("ffmpeg_ss")

        res: SubprocessResult = await web_video(
            path_input=self.path,
            path_output=path_out,
            video_type="webm",
            width=width,
            height=height,
            **kwargs
        )
        return MediaAnimatedMeta.from_path(res.extra)

    async def generate_thumbnail(self, path_out, max_width_or_height: int = 512, **kwargs) -> 'MediaImageMeta':
        from quart_kroket.imaging.imaging import thumbnail_video, SubprocessResult

        kwargs["ffmpeg_ss"] = kwargs.get("ffmpeg_ss", int(self.duration / 2))

        width, height = proportional_scale(
            width=self.width, height=self.height,
            max_width_or_height=max_width_or_height)

        res: SubprocessResult = await thumbnail_video(
            path_input=self.path,
            path_output=path_out,
            width=width,
            height=height,
            **kwargs
        )
        return MediaImageMeta.from_path(res.extra)
