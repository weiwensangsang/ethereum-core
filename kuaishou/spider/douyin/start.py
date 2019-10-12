import pyautogui

from spider.douyin.video_url import get_video_url
from spider.douyin.download import download
from spider.douyin.concatenate import concatenate
from spider.util.util import clickButton, drag, click, pause, moveRel, typeChinese, \
    dragCurrent, movePoint


def get_douyin(keywords, page, concatenate_number, double):
    # 开启模拟器和抓包工具
    start_douyin_app(double)

    data = []
    for item in keywords:
        try:
            app_search(item[1])
            for index in range(page * 1 - 1):
                dragCurrent()

            titles, video_urls = get_video_url(item[1])
            root, paths, titles, keyword = download(titles, video_urls, item[1], 'douyin', concatenate_number)
            m = concatenate(root, paths, titles, keyword)
            data.append(m)
            end_search()
        except Exception:
            continue
    return data


def start_douyin_app(double):
    movePoint('start')
    moveRel(250, 0, 1)
    click(1, 1)
    moveRel(50, 0, 0.1)
    click(1, 8 * double)
    movePoint('lock')
    drag(800, 2)
    pause(5 * double)
    clickButton('Android\\1', 1)
    click(3, 1)
    clickButton('Android\\是', 1)
    pause(5 * double)
    clickButton('Android\\抖音', 1)
    pause(10 * double)
    clickButton('Android\\查找', 1)
    moveRel(0, 60, 0.2)
    click(1, 4)
    moveRel(80, 10, 0.2)
    click(1, 4)


def app_search(data):
    typeChinese(data)
    pause(4)
    clickDouyinSearch()
    pause(4)
    clickButton('Android\\视频', 4)


def end_search():
    clickButton('Android\\下一个', 4)

def clickDouyinSearch():
    movePoint('douyin_search')
    click(1, 1)