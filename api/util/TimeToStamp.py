import time


def to_timestamp(dt, demo="%Y-%m-%d %H:%M:%S"):
    timestamp_ = time.mktime(time.strptime(dt, demo))
    return timestamp_