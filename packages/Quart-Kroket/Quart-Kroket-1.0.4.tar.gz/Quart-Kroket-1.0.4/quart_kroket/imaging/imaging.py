import logging
from dataclasses import dataclass
from typing import Union, Optional
from shutil import which
import asyncio
import re
import os
import sys
import time
import asyncio
from typing import List, Union
from pathlib import Path
from io import BytesIO
from datetime import datetime, timedelta
from dataclasses import dataclass

import magic
import ffmpeg
from PIL import Image
from quart_kroket.media.enums import MediaVideoMeta, MediaImageMeta
import aiofiles


logger = logging.getLogger('root')


class ImageSizeError(Exception):
    pass


async def image_sanitize_resize(
        buffer_or_path: Union[bytes, str],
        path_out: str,
        extension: str, min_size: int, max_size: int, quality: int = 75) -> MediaImageMeta:
    """
    Remove EXIF information, resize if the image is large
    :param buffer_or_path:
    :param path_out:
    :param extension:
    :param min_size: min image width or height, will Exception if below this
    :param max_size: max image width or height, will resize if it exceeds this
    :return:
    """
    if extension not in ["png", "jpg", "jpeg"]:
        raise Exception(f"invalid extension '{extension}'")
    if isinstance(buffer_or_path, str):
        async with aiofiles.open(buffer_or_path, mode='rb') as f:
            buffer = await f.read()
            buffer = BytesIO(buffer)
    elif isinstance(buffer_or_path, bytes):
        buffer = BytesIO(buffer_or_path)
        buffer.seek(0)
    else:
        raise Exception("unknown input")

    image = Image.open(buffer)
    if min([image.height, image.width]) <= min_size:
        raise ImageSizeError("min_size exceeded")
    if max([image.height, image.width]) > max_size:
        image.thumbnail((max_size, max_size), Image.BICUBIC)  # does keep ratio

    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    if extension.lower() == "jpeg":
        if image_without_exif.mode in ["RGBA", "LA"]:
            background = Image.new("RGB", image_without_exif.size, (255, 255, 255))
            try:
                background.paste(image_without_exif, mask=image_without_exif.split()[3])  # 3 is the alpha channel
            except Exception as ex:
                background.paste(image_without_exif, mask=image_without_exif.split()[0])
            image_without_exif = background
        else:
            image_without_exif = image_without_exif.convert('RGB')

    image_without_exif.save(path_out, extension, quality=quality)

    mime = magic.from_file(path_out, mime=True)
    return MediaImageMeta(
        path=path_out,
        width=image_without_exif.width,
        height=image_without_exif.height,
        size=os.path.getsize(path_out),
        mimetype=mime
    )


@dataclass
class SubprocessResult:
    stdout: Union[str, bytes]
    stderr: Union[str, bytes]
    extra: Optional[str]


async def thumbnail_video(
        path_input: str,
        path_output: str,
        ffmpeg_ss: Union[int, str] = None,
        width=512,
        height=512) -> SubprocessResult:
    """
    :param path_input: .mp4 or whatever
    :param path_output: output path
    :param ffmpeg_ss: position where to take the thumbnail image from, in seconds
    :param height: default 512
    :param width: default 512
    :return:
    """
    from quart_kroket.utils import path_temp_name
    logging.debug(f"""{path_input} {path_output} {width}x{height}""".strip())

    if path_input.endswith(".webp"):
        logging.debug("was webp")
        fn_base = path_temp_name()
        fn_webp = fn_base + ".webp"

        cmd_args = [
            which('webpmux'),
            "-get", "frame", "1",
            path_input,
            "-o", fn_webp
        ]

        logging.debug(".webp -> .webp (single frame)")
        logging.debug(" ".join(cmd_args))
        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()

        fn_png = fn_base + ".png"
        cmd_args = [
            which('dwebp'),
            fn_webp,
            "-o", fn_png
        ]

        logging.debug(".webp (single frame) -> .png")
        logging.debug(" ".join(cmd_args))
        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()

        logging.debug(".png -> .jpeg")
        cmd_args = [
            which('convert'),
            fn_png,
            '-resize', f"{width}x{height}",
            '-quality', '75',
            path_output
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()

        logging.debug(f"removing {fn_webp}")
        logging.debug(f"removing {fn_png}")
        os.remove(fn_webp)
        os.remove(fn_png)

        return SubprocessResult(stdout=stdout, stderr=stderr, extra=path_output)

    cmd_args = [
        which('ffmpeg'),
        "-y",
        "-i", path_input,
        "-vframes", "1",
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease"
    ]

    if ffmpeg_ss:
        cmd_args.append("-ss")
        cmd_args.append(str(ffmpeg_ss))

    cmd_args.append(path_output)
    print(" ".join(cmd_args))

    proc = await asyncio.create_subprocess_exec(
        *cmd_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return SubprocessResult(stdout=stdout, stderr=stderr, extra=path_output)


async def web_video(
        path_input: str,
        path_output: str,
        video_type: str = "webm",
        ffmpeg_ss: Optional[Union[int, str]] = 1,
        duration: Optional[int] = None,
        fps: int = 15,
        loop: bool = True,
        enable_audio: bool = False,
        quality: int = 70,
        width=512,
        height=512) -> SubprocessResult:
    """
    generate .gif-like preview thumbnail version of a video
    :param path_input: .mp4 or whatever
    :param path_output: output path
    :param video_type: webm|webp
    :param ffmpeg_ss: position where to start from, default 1 second
    :param duration: .webm duration
    :param fps: default 15
    :param quality: 70
    :param loop: loop .webp
    :param enable_audio:
    :param height: default 512
    :param width: default 512
    :return:
    """
    if fps == 0:
        fps = 15

    cmd_args = [
        which('ffmpeg'),
        "-y",
        "-i", path_input,
        "-q:v", str(quality),
        "-vf", f"fps={fps}, scale={width}:-1"
    ]

    codec = "libwebp" if video_type == "webp" else "libvpx-vp9"
    if path_output.endswith(".webm") and video_type != "webm":
        raise Exception(f"path \"{path_output}\" does not end with .webm")
    elif path_output.endswith(".webp") and video_type != "webp":
        raise Exception(f"path \"{path_output}\" does not end with .webp")

    cmd_args.append("-vcodec")
    cmd_args.append(codec)

    if enable_audio:
        cmd_args.append("-c:a")
        cmd_args.append("libopus")

    if duration:
        cmd_args.append("-t")
        cmd_args.append(str(duration))

    if ffmpeg_ss:
        cmd_args.append("-ss")
        cmd_args.append(str(ffmpeg_ss))

    cmd_args.append(path_output)

    if video_type == "webp":
        cmd_args.append("-loop")
        cmd_args.append("0")
    elif video_type == "webm":
        cmd_args.append("-stream_loop")
        cmd_args.append("-1")

    print(" ".join(cmd_args))
    proc = await asyncio.create_subprocess_exec(
        *cmd_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return SubprocessResult(stdout=stdout, stderr=stderr, extra=path_output)
