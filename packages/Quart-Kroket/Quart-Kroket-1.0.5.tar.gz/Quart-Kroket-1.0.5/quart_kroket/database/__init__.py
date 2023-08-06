import peewee as pw
from peewee import PostgresqlDatabase, SqliteDatabase, ProgrammingError
from playhouse.shortcuts import ReconnectMixin


class ReconnectingPGDatabase(ReconnectMixin, PostgresqlDatabase):
    def __init__(self, *args, **kwargs):
        import peewee as pw
        super(ReconnectingPGDatabase, self).__init__(*args, **kwargs)
        self._reconnect_errors = {
            pw.InterfaceError: ["connection already closed"]
        }


def create_db(user: str, passwd: str, db_name: str, host: str = '127.0.0.1', port: int = 5432) -> ReconnectingPGDatabase:
    return ReconnectingPGDatabase(
        db_name,
        autorollback=True,
        user=user,
        password=passwd,
        host=host,
        port=port
    )


class EnumField(pw.IntegerField):
    def __init__(self, choices, *args, **kwargs):
        super(pw.IntegerField, self).__init__(*args, **kwargs)
        self.choices = choices

    def db_value(self, value):
        if isinstance(value, int):
            return value
        return value.value

    def python_value(self, value):
        return self.choices(value)
