# import os
# import time
import configparser
import random

# from kuaishou.upload import upload
from spider.douyin.start import get_douyin, end_search
from spider.kuaishou.start import get_kuaishou
from spider.util.message import Message
from spider.util.upload import upload_to_bilibili, upload_to_youtube, lauch_chrome, upload_single_file_to_youtube


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

    #kuaishou = get_kuaishou(keywords, page)
    # kuaishou_add_english = map(trans, kuaishou)
    douyin = get_douyin(keywords, page)
    # douyin_add_english = map(trans, douyin)

    # for item in douyin_add_english:
    #     print(item.title)
    #     print(item.tag)
    #     print(item.location)
    #     print(item.desc)
    #     print(item.type)
    # # Todo 开启视频上传流程

    kuaishou = []
    upload_to_bilibili(kuaishou, douyin)
    upload_to_youtube(kuaishou, douyin)

    # upload()
