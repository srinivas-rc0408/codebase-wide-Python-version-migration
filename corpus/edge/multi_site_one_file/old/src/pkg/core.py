from datetime import datetime, timedelta


def stamp():
    return datetime.utcnow()


def window():
    start = datetime.utcnow()
    return start, start + timedelta(hours=1), datetime.utcnow()


def ages(values):
    return [datetime.utcnow() - v for v in values]
