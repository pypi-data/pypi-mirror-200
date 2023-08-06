from copy import deepcopy
from dataclasses import dataclass, is_dataclass

from quart_kroket.data.structures import dict_compare


@dataclass
class PeeweeDirtyFields:
    added: set
    removed: set
    modified: dict
    same: set


import peewee as pw


class PeeweeBaseModel(pw.Model):
    """Has support for better 'dirty field detection'
    takes a performance hit

    @TODO: dont think this works currently

    @TODO: doesnt work when used like this:
       m = model.find_by_uid()
       m.changeme = 3
       m.is_dirty()
    """
    def __init__(self, **kwargs):
        super(PeeweeBaseModel, self).__init__(**kwargs)
        self._initial_data = deepcopy(self.__data__)

    def is_dirty(self) -> PeeweeDirtyFields:
        """added, removed, modified, same = model.is_dirty()"""
        added, removed, modified, same = dict_compare(self._initial_data, self.__data__.copy())
        return PeeweeDirtyFields(added=added, removed=removed, modified=modified, same=same)

