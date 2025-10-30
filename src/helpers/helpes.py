import datetime


def get_now_iso_format():
    return datetime.datetime.now(datetime.UTC).isoformat()
