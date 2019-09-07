import os

import requests

from util.logUtil import debug
from util.logUtil import file


def download(data, keyword, page):
    print(debug(), '视频链接解析成功，开始简介创建...')
    msg = ''
    for item in data:
        msg += item.info() + '\n'
    root = "..\\kuaishou\\resource\\" + file() + keyword + "第" + page + "页\\"
    if os.path.exists(root):
        for f in os.listdir(root):
            path_file2 = os.path.join(root, f)
            if os.path.isfile(path_file2):
                os.remove(path_file2)
        os.removedirs(root)
    os.mkdir(root)
    create__file(root + file() + keyword + "第" + page + "页.txt", msg)
    print(debug(), '简介创建成功，开始视频下载...')
    download_video(data, root)


def create__file(file_path, msg):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path, "a", encoding="utf-8")
    f.write(msg)
    f.close()


def download_video(data, root):
    for item in data:
        name = item.caption[0:20]
        print(debug(), "视频下载:%s" % name)
        r = requests.get(item.url, stream=True)
        with open(root + name + ".mp4", "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)
    print(debug(), "%d个视频下载成功，开始视频处理..." % len(data))
    return
