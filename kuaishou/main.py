# import os
# import time
import configparser
import random

# from kuaishou.upload import upload
from spider.douyin.start import get_douyin
from spider.util.message import Message


def trans(m):
    return Message('English', m.location, m.title, m.tag, m.desc)


if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("resource\\keyword.conf", encoding='utf-8')
    keywords = cf.items("keyword")
    pages = cf.items("page")
    random.shuffle(keywords)
    random.shuffle(pages)
    page = pages[0][1]

    # kuaishou = get_kuaishou(keywords, page)
    # kuaishou_english = map(trans, kuaishou)
    douyin = get_douyin(keywords, page)
    # kdouyin_english = map(trans, douyin)
    # Todo 开启鼠标操作视频上传流程

    # upload()
