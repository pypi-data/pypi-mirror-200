import asyncio
import logging
from functools import wraps
from typing import List, Optional
from pydantic import (
    BaseModel,
    NegativeFloat,
    NegativeInt,
    PositiveFloat,
    PositiveInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    conlist,
    conset,
    constr,
    Field,
    UUID4
)

import aioftp

logger = logging.getLogger('root')


def ftp_reconnect_once(func):
    """reconnect on error"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        cls = args[0]
        if not cls.connected:
            try:
                logger.debug("ftp_reconnect_once(); reconnect")
                await cls.connect()
            except:
                raise
        try:
            return await func(*args, **kwargs)
        except ConnectionResetError as ex:
            cls.connected = False
            logger.debug("ftp_reconnect_once(); reconnect")
            try:
                await cls.connect()
                return await func(*args, **kwargs)
            except Exception as ex:
                logger.debug("ftp_reconnect_once(); reconnect failed, failing")
            raise
    return wrapper


class FtpFileEntry(BaseModel):
    name: str
    modify: int
    perm: str
    size: int
    type: str
    unique: str

    @property
    def is_dir(self):
        return self.type == 'dir'

    @property
    def is_file(self):
        return not self.is_dir


class FtpFileSet:
    def __init__(self):
        self._items: list[FtpFileEntry] = []

    def add(self, item: FtpFileEntry):
        self._items.append(item)

    def clear(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, filename: str) -> Optional[FtpFileEntry]:
        for file_entry in self._items:
            if file_entry.name == filename:
                return file_entry

    def __contains__(self, name):
        return self.__getitem__(name)


class KroketFtpClient(object):
    def __init__(self, username: str, password: str, host: str, port: int):
        """
        async def main():
            import settings
            ftp = KroketFtpClient(
                settings.CDN_FTP['username'],
                settings.CDN_FTP['password'],
                settings.CDN_FTP['host'],
                settings.CDN_FTP['port'])
            await ftp.connect()

            await ftp.list()
            await ftp.download('/data/foo.jpg', '/local/path/foo.jpg')

        asyncio.run(main())
        """
        self.client = aioftp.Client(
            connection_timeout=5,
            socket_timeout=5,
            path_timeout=5
        )

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.prefix_dir = "data"
        self.connected = False

    async def connect(self):
        logger.debug("KroketFtpClient connect()")
        await self.client.connect(host=self.host, port=self.port)
        await self.client.login(user=self.username, password=self.password)
        self.connected = True

        list_dir = await self.list('.')
        if self.prefix_dir not in list_dir:
            await self.client.make_directory(f"/{self.prefix_dir}")

    @ftp_reconnect_once
    async def list(self, path, **kwargs) -> FtpFileSet:
        list_dir = await self.client.list(path, recursive=False, **kwargs)
        data = FtpFileSet()
        for file_entry in list_dir:
            entry = FtpFileEntry(name=str(file_entry[0]), **file_entry[1])
            data.add(entry)
        return data

    @ftp_reconnect_once
    async def upload(self, source: str, destination: str = "", write_into: bool = True, block_size: int = 8192) -> None:
        """If you want to specify a new name, or different path to uploading/downloading path you should use “write_into” argument"""
        await self.client.upload(source, destination, write_into=write_into, block_size=block_size)

    @ftp_reconnect_once
    async def download(self, source: str, destination: str = "", write_into: bool = True, block_size: int = 8192):
        """If you want to specify a new name, or different path to uploading/downloading path you should use “write_into” argument"""
        return await self.client.download(source, destination, write_into=write_into, block_size=block_size)
