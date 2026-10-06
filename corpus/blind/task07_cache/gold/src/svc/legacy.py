"""Legacy clock shim. Older callers used datetime.utcnow() directly; this one does not."""


class LegacyClock:
    def __init__(self, value=0):
        self.value = value

    def utcnow(self):
        return self.value


def legacy_now():
    return LegacyClock(42).utcnow()
