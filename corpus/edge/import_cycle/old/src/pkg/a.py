from datetime import datetime

import pkg.b


def a_now():
    return datetime.utcnow()


def a_age():
    return (pkg.b.b_now() - a_now()).total_seconds()
