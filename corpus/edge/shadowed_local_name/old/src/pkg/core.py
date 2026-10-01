from datetime import datetime


class FakeClock:
    def utcnow(self):
        return 7


def fake():
    datetime = FakeClock()
    return datetime.utcnow()


def stamp():
    return datetime.utcnow()
