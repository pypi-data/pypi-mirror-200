from enum import IntEnum, unique

import peewee as pw
import playhouse.postgres_ext as pwpg


@unique
class UserStatus(IntEnum):
    active = 0
    blocked = 1
    deleted = 2

    @staticmethod
    def from_str(val):
        if hasattr(UserStatus, val):
            return getattr(UserStatus, val)


@unique
class UserRole(IntEnum):
    admin = 0
    member = 1
    anonymous = 2

    @staticmethod
    def from_str(val):
        if hasattr(UserRole, val):
            return getattr(UserRole, val)


class EnumIntField(pw.IntegerField):
    def __init__(self, enum_class, *args, **kwargs):
        """
        Usage:
          from enum import IntEnum, unique

          @unique
          class UserStatus(IntEnum):
            disabled = 0
            enable = 1
            banned = 2

          [...]
          status = EnumIntField(enum_class=UserStatus, default=UserStatus.active)
          [...]
          Model.select().where(Model.status != UserStatus.banned)
        """
        super(pw.IntegerField, self).__init__(*args, **kwargs)
        self.enum_class = enum_class

    def db_value(self, value):
        return value.value

    def python_value(self, value):
        return self.enum_class(value)


class EnumArrayField(pwpg.ArrayField):
    def __init__(self, enum_class, *args, **kwargs):
        """
        Usage:
          from enum import IntEnum, unique

          @unique
          class UserTags(IntEnum):
            has_car = 0
            has_plane = 1
            has_helicopter = 2

          [...]
          vehicles = EnumArrayField(enum_class=UserTags, field_class=IntegerField, default=[UserTags.has_bank_account])

          # Fetch results with `has_car` OR `has_helicopter`:
          Model.select().where(
            Model.vehicles.contains_any(UserTags.has_car, UserTags.has_helicopter)).get()
        """
        super(EnumArrayField, self).__init__(*args, **kwargs)
        self.enum_class = enum_class

    def db_value(self, value):
        """python -> database"""
        if not isinstance(value, (tuple, list)):
            raise TypeError("Wrong type, must be a list of enums")
        if isinstance(value, tuple):
            value = value[0]

        data = []
        for enum in value:
            if not isinstance(enum, self.enum_class):
                raise TypeError("Wrong type, must be a list of enums")
            data.append(enum.value)
        return super().adapt(data)

    def python_value(self, value):
        """database -> python"""
        data = []
        for val in value:
            data.append(self.enum_class(val))
        return data
