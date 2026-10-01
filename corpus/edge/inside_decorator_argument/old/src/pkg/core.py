from datetime import datetime


def tagged(when):
    def wrap(f):
        f.when = when
        return f
    return wrap


@tagged(datetime.utcnow())
def job():
    return 1
