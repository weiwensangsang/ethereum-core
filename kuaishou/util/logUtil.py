import datetime


def debug():
    return datetime.datetime.now().strftime('%H:%M:%S')


def file():
    return datetime.datetime.now().strftime('%Y-%m-%d')
