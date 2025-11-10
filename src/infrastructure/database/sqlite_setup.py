import datetime
import sqlite3


def _convert_timestamp(val):
    if val is None:
        return None
    return datetime.datetime.fromisoformat(val.decode())


def _adapt_datetime(ts):
    return ts.isoformat(" ")


def setup_sqlite_converters():
    sqlite3.register_converter("timestamp", _convert_timestamp)
    sqlite3.register_adapter(datetime.datetime, _adapt_datetime)
