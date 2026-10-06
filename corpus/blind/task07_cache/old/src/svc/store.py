"""Persist the last stamp to a JSON file and read it back."""

import datetime
import json

from svc.stamp import stamp


def save(path):
    value = stamp()
    with open(path, "w") as handle:
        json.dump({"stamp": value.isoformat()}, handle)
    return value


def load(path):
    with open(path) as handle:
        s = json.load(handle)["stamp"]
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
