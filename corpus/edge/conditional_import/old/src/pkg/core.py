try:
    from datetime import UTC, datetime
except ImportError:  # Python < 3.11
    from datetime import datetime

    UTC = None


def stamp():
    return datetime.utcnow()
