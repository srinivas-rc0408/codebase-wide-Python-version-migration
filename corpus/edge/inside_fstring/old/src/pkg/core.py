from datetime import datetime


def label():
    return f"at {datetime.utcnow():%Y}"
