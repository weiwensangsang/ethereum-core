from spider.douyin.douyin_video_url import get_video_url
from spider.douyin.download import download
from spider.util.util import clickButton, drag, click, pause, moveRel, typeChinese, \
    dragCurrent


def get_douyin(keywords, page):
    # 开启模拟器和抓包工具
    start_douyin_app()

    data = []
    for item in keywords[0:1]:
        app_search(item[1])
        for index in range((int(page) + 1) * 1):
            dragCurrent()

        titles, video_urls = get_video_url(item[1])
        download(titles, video_urls, item[1], 'douyin')
        #m = concatenate(vm)
    return data


def start_douyin_app():
    clickButton('抓包', 1)
    moveRel(50, 0, 0.1)
    click(1, 30)
    drag('Android\\锁', 800, 2)
    clickButton('Android\\1', 1)
    click(3, 1)
    clickButton('Android\\是', 1)
    clickButton('Android\\抖音', 1)
    pause(10)
    clickButton('Android\\查找', 1)
    moveRel(0, 60, 0.2)
    click(1, 4)
    moveRel(80, 10, 0.2)
    click(1, 4)


def app_search(data):
    typeChinese(data)
    clickButton('Android\\搜索', 4)
    clickButton('Android\\视频', 4)

