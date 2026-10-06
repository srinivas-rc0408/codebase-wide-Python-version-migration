"""Is a cached session still fresh?"""

from svc.stamp import stamp
from svc.store import load


def is_fresh(path, max_age_s):
    return (stamp() - load(path)).total_seconds() < max_age_s
