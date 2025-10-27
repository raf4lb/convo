from datetime import datetime


def get_now_iso_format():
    return datetime.now().isoformat()
