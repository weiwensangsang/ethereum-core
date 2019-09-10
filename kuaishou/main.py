# import os
# import time
import configparser
import random
import sys

#from util.upload import upload
from util.message import Message
from util.video_concatenate import concatenate
from util.video_download import download
from util.video_url import get_video_url

if __name__ == "__main__":


    cf = configparser.ConfigParser()
    cf.read("resource\\keyword.conf", encoding='utf-8')
    keywords = cf.items("keyword")
    pages = cf.items("page")
    random.shuffle(keywords)
    random.shuffle(pages)
    page = pages[0][1]
    chinese = []
    english = []
    for item in keywords[0:3]:
        video_urls = []
        for index in range(int(page)):
            video_urls.extend(get_video_url(item[1], str(index)))
        vm = download(video_urls, item[1])
        m = concatenate(vm)
        chinese.append(m)
        english.append(Message('English', m.location, m.title, m.tag, m.decs))
    #Todo 开启鼠标操作流程


    #upload()

