import aiohttp


async def get_http(url, headers=None, timeout=4, raise_for_status=True):
    timeout = aiohttp.ClientTimeout(total=timeout)
    if not headers:
        headers = {}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if raise_for_status:
                resp.raise_for_status()
                return await resp.text()


async def get_json(url, headers=None, timeout=4, raise_for_status=True):
    timeout = aiohttp.ClientTimeout(total=timeout)
    if not headers:
        headers = {}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if raise_for_status:
                resp.raise_for_status()
                return await resp.json()


async def post_json(url, data: dict, headers=None, timeout=4, raise_for_status=True):
    timeout = aiohttp.ClientTimeout(total=timeout)
    if not headers:
        headers = {}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=data, headers=headers) as resp:
            if raise_for_status:
                resp.raise_for_status()
            return await resp.json()
