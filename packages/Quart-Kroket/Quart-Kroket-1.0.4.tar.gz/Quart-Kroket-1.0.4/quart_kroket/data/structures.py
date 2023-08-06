from typing import Annotated, List
from dataclasses import dataclass, is_dataclass


def dataclass_from_dict_nested(schema: any, data: dict):
    """
    Turns a dict back into a dataclass *with* support for nesting

    @dataclass
    class test2:
        a: str = 'name'
        b: int = 222

    @dataclass
    class test:
        a: str = 'name'
        b: int = 222
        t: test2 = None

    a = test(a = 2222222222, t=test2(a="ssss"))
    print(a)

    result = dataclass_from_dict_nested(test, {'a': 1111111, 't': {'a': 'nazwa'} })
    """
    data_updated = {
        key: (
            data[key]
            if not is_dataclass(schema.__annotations__[key])
            else dataclass_from_dict_nested(schema.__annotations__[key], data[key])
        )
        for key in data.keys()
    }
    return schema(**data_updated)


def dict_compare(d1, d2) -> tuple[set, set, dict, set]:
    """
        x = dict(a=1, b=2)
        y = dict(a=2, b=2)
        added, removed, modified, same = dict_compare(x, y)
    :param d1:
    :param d2:
    :rtype: (set, set, dict, set)
    :return: added, removed, modified, same
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same
