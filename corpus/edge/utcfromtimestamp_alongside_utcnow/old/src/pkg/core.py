from datetime import datetime


def stamp():
    return datetime.utcnow()


def from_epoch(t):
    return datetime.utcfromtimestamp(t)
