from typing import Optional
import asyncio
import os

import aiohttp


async def gravatar_download(hash: str, timeout: int = 5) -> Optional[bytes]:
    """Download image, return bytes

    Feel free to write it to disk:
        import aiofiles

        dest = os.path.join(cache_dir, filename)
        async with aiofiles.open(dest, mode='wb') as f:
            await f.write(data)
    """
    url = f'https://www.gravatar.com/avatar/{hash}'

    timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            content_type = resp.headers.get('content-type')
            if not content_type.startswith("image"):
                raise Exception("gravatar failure")
            data: bytes = await resp.content.read()
            return data
