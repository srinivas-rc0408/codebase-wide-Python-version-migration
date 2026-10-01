from datetime import datetime, timezone


def stamp():
    return datetime.now(timezone.utc)


def legacy():
    return datetime.utcnow()
