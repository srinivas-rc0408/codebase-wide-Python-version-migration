from datetime import datetime

import pkg.a


def b_now():
    return datetime.utcnow()


def b_age():
    return (pkg.a.a_now() - b_now()).total_seconds()
