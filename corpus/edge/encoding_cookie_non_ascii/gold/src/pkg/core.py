# -*- coding: latin-1 -*-
"""Zeitstempel für Größen."""
from datetime import datetime, timezone

größe = "maß"


def stamp():
    return datetime.now(timezone.utc)
