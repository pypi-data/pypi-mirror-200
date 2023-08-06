import asyncio
import hashlib
import os
from shutil import which

from quart import current_app
from quart_kroket.utils import program_exists


def md5_string(inp: bytes):
    return hashlib.md5(inp).hexdigest()


async def sha256sum(path_to_file: str) -> str:
    if not program_exists('sha256sum'):
        raise Exception("Could not find 'sha256sum' in PATH")
    if not os.path.isfile(path_to_file):
        raise Exception(f"Could not find file '{path_to_file}'")

    p = await asyncio.create_subprocess_exec(
        which('sha256sum'), path_to_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True
    )

    stdout_data, stderr_data = await p.communicate()
    if p.returncode == 0:
        try:
            checksum = stdout_data.split(b' ')[0].strip()
            if len(checksum) == 64:
                return checksum.decode()
        except Exception as ex:
            current_app.logger.error(f"sha256sum error: {stdout_data} | {ex}")

    raise Exception(f"Error executing sha256sum'; {stdout_data} - {stderr_data}")
