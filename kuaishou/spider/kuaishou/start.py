from spider.kuaishou.concatenate import concatenate
from spider.kuaishou.download import download
from spider.kuaishou.video_url import get_video_url


def get_kuaishou(keywords, page):
    data = []
    for item in keywords[0:3]:
        video_urls = []
        for index in range(int(page)):
            video_urls.extend(get_video_url(item[1], str(index)))
        vm = download(video_urls, item[1])
        #m = concatenate(vm)
        #data.append(m)
    return data
