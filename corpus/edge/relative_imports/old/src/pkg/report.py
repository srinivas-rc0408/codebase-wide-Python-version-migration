from datetime import datetime

from .core import stamp


def age():
    return (datetime.utcnow() - stamp()).total_seconds()
