import os
import asyncio
from typing import Optional, Union
from shutil import which

from quart_kroket.utils import program_exists


async def pdf_to_img(path_to_pdf: str, path_output: str) -> Union[str, os.PathLike]:
    if not program_exists('pdftoppm'):
        raise Exception("Could not find 'pdftoppm' in PATH")
    if not os.path.isfile(path_to_pdf):
        raise Exception(f"Could not find file '{path_to_pdf}'")

    p = await asyncio.create_subprocess_exec(
        which('pdftoppm'), path_to_pdf, path_output, '-png', '-singlefile',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True
    )

    stdout_data, stderr_data = await p.communicate()
    if p.returncode == 0 and os.path.isfile(path_output + ".png"):
        return path_output + ".png"

    raise Exception(f"Error while writing to '{path_output}.png'; {stdout_data} - {stderr_data}")


async def pdf_to_text(path_to_pdf: str) -> Optional[bytes]:
    if not program_exists('pdftotext'):
        raise Exception("Could not find 'pdftotext' in PATH")
    if not os.path.isfile(path_to_pdf):
        raise Exception(f"Could not find file '{path_to_pdf}'")

    p = await asyncio.create_subprocess_exec(
        which('pdftotext'), path_to_pdf, '-raw', '-',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True
    )

    stdout_data, stderr_data = await p.communicate()
    if p.returncode == 0:
        return stdout_data
