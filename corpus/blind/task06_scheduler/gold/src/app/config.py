"""Static configuration."""

import datetime as dtm

EPOCH = dtm.datetime(2020, 1, 1, tzinfo=dtm.timezone.utc)


def boot_time():
    return dtm.datetime.fromtimestamp(0, dtm.timezone.utc)
