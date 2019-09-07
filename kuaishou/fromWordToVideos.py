# import os
# import time

import sys

from util.httpClient import getVideoUrls

if __name__ == "__main__":
    keyword = sys.argv[1]
    page = sys.argv[2]
    getVideoUrls(keyword, page)
