from datetime import datetime, timezone


def stamp() -> datetime:
    return datetime.now(timezone.utc)
