# import os
# import time

import sys

from util.video_download import download
from util.video_url import get_video_url
from util.video_concatenate import concatenate

if __name__ == "__main__":
    keyword = sys.argv[1]
    page = sys.argv[2]
    video_urls = get_video_url(keyword, page)
    videos = download(video_urls, keyword, page)
    concatenate(videos)
