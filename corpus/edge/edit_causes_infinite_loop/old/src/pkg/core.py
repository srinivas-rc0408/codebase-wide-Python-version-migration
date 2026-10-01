from datetime import datetime


def wait_for(deadline):
    while True:
        try:
            if datetime.utcnow() >= deadline:
                return
        except TypeError:  # aware vs naive: retries forever
            continue
