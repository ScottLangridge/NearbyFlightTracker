import datetime


def nullable_datetime(epoch):
    if epoch is None:
        return None
    else:
        return datetime.datetime.fromtimestamp(epoch)
