# import os
# import time

import sys

from util.download import download
from util.spider import getVideoUrls

if __name__ == "__main__":
    keyword = sys.argv[1]
    page = sys.argv[2]
    data = getVideoUrls(keyword, page)
    download(data, keyword, page)
