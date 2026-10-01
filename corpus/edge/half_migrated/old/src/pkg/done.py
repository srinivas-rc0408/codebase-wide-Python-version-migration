from datetime import datetime, timezone


def ok():
    return datetime.now(timezone.utc)
