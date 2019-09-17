import requests
from moviepy.editor import *

from spider.util.util import date, VM
from spider.util.util import now


def download(data, keyword, type):
    print(now(), '视频链接解析成功，开始简介创建...')
    decs = ''
    title = ''
    i = 1
    for item in data:
        if i == 1:
            title = item.info()
        decs += item.info() + '\n'
        i += 1
    root = "..\\kuaishou\\resource\\" + type + '\\' + date() + "_" + keyword + "\\"
    if os.path.exists(root):
        for f in os.listdir(root):
            path_file2 = os.path.join(root, f)
            if os.path.isfile(path_file2):
                os.remove(path_file2)
        os.removedirs(root)
    os.mkdir(root)
    #create__file(root + title + ".txt", decs)
    print(now(), '简介创建成功，开始视频下载...')
    return download_video(data, root, title, keyword, decs)


def create__file(file_path, msg):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path, "a", encoding="utf-8")
    f.write(msg)
    f.close()


def download_video(data, root, title, keyword, decs):
    #data = data[0:2]
    for item in data:
        name = item.caption[0:20]
        print(now(), "视频下载:%s" % name)
        r = requests.get(item.url, stream=True)
        item.path_name = root + name + ".mp4";
        with open(item.path_name, "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)
    print(now(), "%d个视频下载成功" % len(data))
    return VM(data, title, keyword, decs)
