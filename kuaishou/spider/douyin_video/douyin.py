from spider.kuaishou_video.video_concatenate import concatenate
from spider.kuaishou_video.video_download import download
from spider.kuaishou_video.video_url import get_video_url
from spider.util.util import clickButton, drag, typeEnter, typeWords, click, pause, moveTo, moveRel, typeChinese
import pyautogui


def get_douyin(keywords, page):
    # 开启模拟器和抓包工具
    start_douyin_app()

    data = []
    for item in keywords[0:3]:
        video_urls = []
        for index in range(int(page)):
            video_urls.extend(get_video_url(item[1], str(index)))
        vm = download(video_urls, item[1])
        m = concatenate(vm)
        data.append(m)
    return data


def start_douyin_app():
    clickButton('抓包', 4)
    clickButton('Android\\Android', 30)
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


def drag_feed():
    moveRel(0, 300, 1)
    pyautogui.dragRel(0, -300, button='left')  # 绝对移动


if __name__ == "__main__":

    start_douyin_app()
    video_urls = []
    app_search('美女')
    for index in range(3 * 3):
        drag_feed()
    # for index in range(int(page)):
    # video_urls.extend(get_video_url(item[1], str(index)))
