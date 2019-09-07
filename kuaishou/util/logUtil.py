import datetime


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')
