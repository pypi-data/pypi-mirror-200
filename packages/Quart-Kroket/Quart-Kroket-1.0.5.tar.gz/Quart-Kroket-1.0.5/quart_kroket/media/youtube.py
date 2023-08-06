import json
import os
import sys
import asyncio
import re
from dataclasses import dataclass
from typing import Optional

from quart_kroket.media.enums import MediaMusicMeta


RE_YOUTUBE = r"[a-zA-Z0-9_-]{11}$"


class YouTube:
    @staticmethod
    async def download(
            utube_id: str,
            output_dir: str,
            max_duration: int = 600) -> Optional['MediaMusicMeta']:
        """
        Download from YouTube into .ogg
        :param utube_id:
        :param output_dir: path to a directory
        :param max_duration: 10 minutes
        :return:
        """
        if not os.path.isdir(output_dir):
            raise Exception(f"output_dir ({output_dir}) not a dir")
        if not YouTube.is_valid_uid(utube_id):
            raise Exception("bad utube_id")

        path_output = os.path.join(output_dir, "%(id)s.ogg")

        try:
            proc = await asyncio.create_subprocess_exec(
                *["yt-dlp",
                    "--add-metadata",
                    "--write-all-thumbnails",
                    "--write-info-json",
                    "-f", "bestaudio",
                    "--max-filesize", "30M",
                    "--extract-audio",
                    "--audio-format", "vorbis",
                    "-o", path_output,
                    f"https://www.youtube.com/watch?v={utube_id}"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            result = await proc.communicate()
            result = result[0].decode()
            if "100%" not in result:
                raise Exception("download did not complete")
        except Exception as ex:
            msg = f"download failed: {ex}"
            raise Exception(msg)

        meta = MediaMusicMeta.from_path(path_output)
        if meta.duration > max_duration:
            raise Exception(f"Song exceeded duration of {max_duration} seconds")
        return meta

    @staticmethod
    async def pip_upgrade_yt_dlp():
        pip_path = os.path.join(os.path.dirname(sys.executable), "pip")
        proc = await asyncio.create_subprocess_exec(
            *[sys.executable, pip_path, "install", "--upgrade", "yt-dlp"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        return stdout.decode()

    @staticmethod
    def is_valid_uid(uid: str) -> bool:
        return re.match(RE_YOUTUBE, uid) is not None
