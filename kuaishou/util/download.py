import os

from util.logUtil import debug
from util.logUtil import file


def download(data, keyword, page):
    print(debug(), '视频链接解析成功，开始简介创建...')
    msg = ''
    for item in data:
        msg += item.info() + '\n'
    create__file("..\\kuaishou\\resource\\" + file() + keyword + "第" + page + "页.txt", msg)
    print(debug(), '简介创建成功，开始视频下载...')


def create__file(file_path, msg):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path, "a", encoding="utf-8")
    f.write(msg)
    f.close()
