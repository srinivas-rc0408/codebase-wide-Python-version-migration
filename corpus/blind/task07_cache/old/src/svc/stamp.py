"""The clock every cached session is stamped with."""

import datetime


def stamp():
    return datetime.datetime.utcnow()
