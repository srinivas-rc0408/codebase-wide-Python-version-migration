"""Static configuration."""

import datetime as dtm

EPOCH = dtm.datetime(2020, 1, 1)


def boot_time():
    return dtm.datetime.utcfromtimestamp(0)
