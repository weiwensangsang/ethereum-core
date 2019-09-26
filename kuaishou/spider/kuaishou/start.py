from spider.kuaishou.concatenate import concatenate
from spider.kuaishou.download import download
from spider.kuaishou.video_url import get_video_url


def get_kuaishou(keywords, page, concatenate_number):
    data = []
    for item in keywords:
        video_urls = []
        for index in range(page):
            try:
                video_urls.extend(get_video_url(item[1], str(index)))
            except Exception:
                continue
        vm = download(video_urls, item[1], 'kuaishou', concatenate_number)
        m = concatenate(vm)
        data.append(m)
    return data
