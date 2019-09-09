# import os
# import time
import configparser
import random
import sys

#from util.upload import upload
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
    for item in keywords[0:3]:
        video_urls = []
        for index in range(int(page)):
            video_urls.extend(get_video_url(item[1], str(index)))
        videos = download(video_urls, item[1])
        concatenate(videos)
    #upload()

