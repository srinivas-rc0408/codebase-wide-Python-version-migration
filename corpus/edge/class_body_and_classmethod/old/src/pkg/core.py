from datetime import datetime


class Clock:
    created = datetime.utcnow()

    @classmethod
    def now(cls):
        return datetime.utcnow()
