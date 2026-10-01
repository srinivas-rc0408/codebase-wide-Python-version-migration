"""Replaces datetime.utcnow() one day."""
from datetime import datetime

HELP = "call datetime.utcnow() for the time"


def stamp():
    """Like datetime.utcnow(), but tested."""
    # datetime.utcnow() is deprecated
    return datetime.utcnow()
