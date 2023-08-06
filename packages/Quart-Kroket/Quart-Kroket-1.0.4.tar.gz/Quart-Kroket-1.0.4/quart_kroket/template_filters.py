import hashlib
from datetime import datetime

import humanize


def hash_sha256(val: str):
    if not val:
        return ""
    return hashlib.sha256(val.encode()).hexdigest()


def hash_md5(val: str):
    if not val:
        return ""
    return hashlib.md5(val.encode()).hexdigest()


def size_human(val: str):
    return humanize.naturalsize(val)


def dt_ago(val: datetime):
    val = val.replace(tzinfo=None)
    return humanize.naturaltime(datetime.now() - val)


def dt_human(val: datetime):
    return val.strftime('%Y-%m-%d %H:%M')


func_map = {
    'dt_human': dt_human,
    'dt_ago': dt_ago,
    'size_human': size_human,
    'hash_md5': hash_md5,
    'hash_sha256': hash_sha256
}
