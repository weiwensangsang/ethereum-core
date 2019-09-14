import requests
from moviepy.editor import *

from spider.util.util import file_time, VM, get_trans
from spider.util.util import now


def download(titles, video_urls, keyword, type):
    print(now(), '视频链接解析成功，开始简介创建...')
    root = "..\\kuaishou\\resource\\" + type + '\\' + file_time() + "_" + keyword + "\\"
    if os.path.exists(root):
        for f in os.listdir(root):
            path_file2 = os.path.join(root, f)
            if os.path.isfile(path_file2):
                os.remove(path_file2)
        os.removedirs(root)
    os.mkdir(root)
    #create__file(root + title + ".txt", decs)
    print(now(), '简介创建成功，开始视频下载...')
    return download_video(video_urls, root, keyword, titles)


def create__file(file_path, msg):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path, "a", encoding="utf-8")
    f.write(msg)
    f.close()


def download_video(video_urls, root, keyword, titles):
    video_urls = video_urls[0:2]
    index = 0
    paths = []
    for item in video_urls:
        #print(titles[index])
        name = titles[index].split('记录美好生活')[1].split('%s 复制此链接')[0].translate(get_trans()).replace('#', '')
        titles[index] = name
        print(now(), "视频下载:%s" % name)
        r = requests.get(item, stream=True)
        path = root + name + ".mp4";
        paths.append(path)
        with open(path, "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)
        index = index + 1
    print(now(), "%d个视频下载成功" % len(video_urls))
    return root, paths, titles, keyword
