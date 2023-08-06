import time, os, stat, string, tempfile
from functools import wraps
from shutil import which
from random import random, SystemRandom


def file_age_in_seconds(pathname) -> float:
    return time.time() - os.stat(pathname)[stat.ST_MTIME]


def make_slug(inp: str) -> str:
    from slugify import slugify
    return slugify(inp, max_length=32)


def program_exists(name: str):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def safu(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            print(f"safu error: {ex}")
    return wrapper


def get_visitor_ipv4(enforce_forwarded_header=True):
    """Note: only use when Quart is reverse proxied"""
    from quart import request, current_app
    if 'X-Forwarded-For' not in request.headers:
        msg = "X-Forwarded-For header not set by the reverse proxy!"
        current_app.logger.warning(msg)
        if enforce_forwarded_header:
            raise Exception(msg)
    return request.headers.get('X-Forwarded-For', '127.0.0.1')


def random_str(num_chars: int):
    return ''.join(
        SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(num_chars))


def path_temp_name() -> str:
    """generate temporary tmp path"""
    temp_name = next(tempfile._get_candidate_names())
    tmp_dir = tempfile._get_default_tempdir()
    return f"{tmp_dir}/{temp_name}"
