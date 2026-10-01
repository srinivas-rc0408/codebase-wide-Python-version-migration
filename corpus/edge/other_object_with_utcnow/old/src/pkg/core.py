from datetime import datetime


class Clock:
    def utcnow(self):
        return 42


clock = Clock()


def fake():
    return clock.utcnow()


def stamp():
    return datetime.utcnow()
