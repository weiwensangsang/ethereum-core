# import os
# import time
import configparser
import os

# from kuaishou.upload import upload
from spider.douyin.start import get_douyin
from spider.kuaishou.start import get_kuaishou
from spider.util.message import Message
from spider.util.upload import upload_to_bilibili, upload_to_youtube
from spider.util.util import clean_start_workspace


def get_data():
    root_douyin = "resource\\douyin"
    root_kuaishou = "resource\\kuaishou"

    if os.path.exists("resource\\douyin"):
        clean_start_workspace('douyin')
    if os.path.exists("resource\\kuaishou"):
        clean_start_workspace('kuaishou')

    os.mkdir(root_douyin)
    os.mkdir(root_kuaishou)

    cf = configparser.ConfigParser()
    cf.read("resource\\keyword.conf", encoding='utf-8')
    basic_keyword = cf.items("keyword")
    config = cf.items("config")
    page = int(config[0][1])
    keyword_number = int(config[1][1])
    concatenate_number = int(config[2][1])
    index = int(cf.items("current")[0][1])
    # print(index)
    # print(len(basic_keyword))
    if (index + keyword_number) > len(basic_keyword):
        index = 0
    keywords = cf.items("keyword")[index: index + keyword_number]
    index = index + keyword_number
    cf.set("current", "index", str(index))

    with open("resource\\keyword.conf", "w+", encoding='utf-8') as f:
        cf.write(f)
    return keywords, page, concatenate_number


if __name__ == "__main__":
    keywords, page, concatenate_number = get_data()
    #print(keywords, page, concatenate_number)

    kuaishou = get_kuaishou(keywords, page, concatenate_number)
    douyin = get_douyin(keywords, page, concatenate_number, 10)


    upload_to_bilibili(kuaishou, douyin)
    upload_to_youtube(kuaishou, douyin)

