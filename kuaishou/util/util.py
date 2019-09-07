import datetime


def time():
    return datetime.datetime.now().strftime('%H:%M:%S')


def file_time():
    return datetime.datetime.now().strftime('%Y-%m-%d')
