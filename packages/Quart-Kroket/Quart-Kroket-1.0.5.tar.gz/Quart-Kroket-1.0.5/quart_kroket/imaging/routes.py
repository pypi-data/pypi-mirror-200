import os
from typing import Union
import hashlib

from quart import Response, send_from_directory
from quart_kroket.imaging import CACHE_DIR_BASE, CACHE_DIR_AVATAR, CACHE_DIR_GRAVATAR, CACHE_DIR_QR
import aiofiles

for _d in [CACHE_DIR_BASE, CACHE_DIR_AVATAR, CACHE_DIR_GRAVATAR, CACHE_DIR_QR]:
    if not os.path.exists(_d):
        os.mkdir(_d)


async def route_imaging_gravatar(inp: str) -> Response:
    return await _generate(inp, _gen_gravatar, CACHE_DIR_GRAVATAR)


async def route_imaging_avatar(inp: str) -> Response:
    return await _generate(inp, _gen_avatar, CACHE_DIR_AVATAR)


async def route_imaging_qr(inp: str, color_from = None, color_to = None) -> Response:
    return await _generate(inp, _gen_qr, CACHE_DIR_QR, color_from=color_from, color_to=color_to)


async def _gen_qr(inp: str, save_path: str, color_from: Union[str, tuple] = None, color_to: Union[str, tuple] = None) -> str:
    from quart_kroket.imaging.qr import QrCodeGen
    from quart_kroket.imaging import QR_COLOR_FROM, QR_COLOR_TO
    if not color_from:
        _color_from = QR_COLOR_FROM
    else:
        _color_from = color_from.split(',')

    if not color_to:
        _color_to = QR_COLOR_TO
    else:
        _color_to = color_to.split(',')
    
    if len(_color_to) != 3 or len(_color_from) != 3:
        raise Exception("wrong array size for color_from or color_to")

    try:
        _color_from = tuple(map(int, _color_from))
        _color_to   = tuple(map(int, _color_to))
    except Exception as ex:
        raise Exception("array elements must be int")

    qr = QrCodeGen()
    img = qr.create(inp, color_from=_color_from, color_to=_color_to)
    img.save(save_path)
    return save_path


async def _gen_gravatar(inp: str, save_path: str) -> str:
    """returns saved filepath"""
    from quart_kroket.data.checksum import md5_string
    from quart_kroket.net.gravatar import gravatar_download

    md5_hash = md5_string(inp.encode())
    data = await gravatar_download(hash=md5_hash)
    async with aiofiles.open(save_path, mode='wb') as f:
        await f.write(data)
    return save_path


async def _gen_avatar(inp: str, save_path: str) -> str:
    """returns saved filepath"""
    from quart_kroket.imaging.avatars import PastelAvatar

    avatar = PastelAvatar(rows=10, columns=10)
    image = avatar.get_image(
        string=inp,
        width=512,
        height=512,
        pad=0)
    image.save(save_path, 'png', quality=90)
    return save_path


async def _generate(inp: str, func, cache_dir: str, cache_ttl=10, **kwargs):
    from quart_kroket.data.checksum import md5_string
    from quart_kroket.utils import file_age_in_seconds

    fn = md5_string(inp.encode()) + ".png"
    dest = os.path.join(cache_dir, fn)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    if os.path.exists(dest):
        secs = file_age_in_seconds(dest)
        if secs <= cache_ttl:
            return await send_from_directory(
                directory=cache_dir,
                file_name=fn
            )

    await func(inp, dest, **kwargs)

    return await send_from_directory(
        directory=cache_dir,
        file_name=fn
    )

