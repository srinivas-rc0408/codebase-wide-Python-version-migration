from datetime import datetime

from pkg.core import stamp


def age_seconds():
    return (datetime.utcnow() - stamp()).total_seconds()
