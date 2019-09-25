from spider.douyin.video_url import get_video_url
from spider.douyin.download import download
from spider.douyin.concatenate import concatenate
from spider.util.util import clickButton, drag, click, pause, moveRel, typeChinese, \
    dragCurrent, movePoint


def get_douyin(keywords, page):
    # 开启模拟器和抓包工具
    start_douyin_app()

    data = []
    for item in keywords[0:4]:
        try:
            app_search(item[1])
            for index in range((int(page)) * 1 - 1):
                dragCurrent()

            titles, video_urls = get_video_url(item[1])
            root, paths, titles, keyword = download(titles, video_urls, item[1], 'douyin')
            m = concatenate(root, paths, titles, keyword)
            data.append(m)
            end_search()
        except Exception:
            continue
    return data


def start_douyin_app():
    movePoint('start')
    moveRel(250, 0, 1)
    click(1, 1)
    moveRel(50, 0, 0.1)
    click(1, 30)
    movePoint('lock')
    drag(800, 2)
    pause(5)
    clickButton('Android\\1', 1)
    click(3, 1)
    clickButton('Android\\是', 1)
    clickButton('Android\\抖音', 1)
    pause(100)
    clickButton('Android\\查找', 1)
    moveRel(0, 60, 0.2)
    click(1, 4)
    moveRel(80, 10, 0.2)
    click(1, 4)


def app_search(data):
    typeChinese(data)
    clickButton('Android\\搜索', 4)
    clickButton('Android\\搜索2', 4)
    clickButton('Android\\视频', 4)


def end_search():
    clickButton('Android\\下一个', 4)