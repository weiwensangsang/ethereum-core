import os

import pyautogui

from spider.util.util import now, clickButton, moveRel, click, typeChinese, typeTab, typeEnter, scroll, \
    movePoint, middleClick, translate, rightClickButton, rightClick, pause, position, date


def upload_to_bilibili(kuaishou, douyin):
    print(now(), '开始上传快手到bilibili...')
    lauch_bilibili_upload()
    for m in kuaishou:
        upload_single_file_to_bilibili(m, "【快手】")

    print(now(), '开始上传抖音到bilibili...')
    for m in douyin:
        upload_single_file_to_bilibili(m, "【抖音】")
    return


def upload_to_youtube(kuaishou, douyin):
    print(now(), '开始设置网络...')
    if not set_good_network():
        print(now(), '网络不稳定，结束上传。')
        return
    print(now(), '网络设置成功，开始上传快手到youtube...')
    for m in kuaishou:
        lauch_chrome()
        upload_single_file_to_youtube(m, "【快手】")
    print(now(), '开始上传抖音到youtube...')
    for m in douyin:
        lauch_chrome()
        upload_single_file_to_youtube(m, "【抖音】")

    return


def lauch_chrome():
    movePoint('start')
    moveRel(350, 0, 1)
    middleClick()

def lauch_bilibili_upload():
    movePoint('start')
    moveRel(450, 0, 1)
    click(1, 1)


def upload_single_file_to_bilibili(message, type):
    path = message.location
    title = type + "【" + message.tag + "】" + message.title + " (" + date() + ")"
    tag = message.tag
    desc = message.desc

    movePoint('bilibili_upload')
    click(1, 1)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    moveRel(190, -190, 1)
    click(1, 1)
    moveRel(-90, 100, 1)
    click(1, 1)

    moveRel(-650, 30, 1)
    click(1, 1)
    scroll(-700)
    moveRel(0, -280, 1)
    click(1, 1)
    typeChinese(title)
    typeTab()
    typeChinese(tag)
    typeEnter()
    moveRel(0, 380, 1)
    click(1, 1)
    typeChinese(desc)
    typeTab()
    typeTab()
    typeTab()
    typeEnter()
    pause(20)


def upload_single_file_to_youtube(message, type):
    base = ['抖音', '快手', 'Tik Tok', 'kuaishou']
    tags= []
    movePoint('page_start')
    moveRel(150, 0, 1)
    click(1, 5)
    path = message.location
    title = type + "【" + message.tag + "】"+ message.title + " (" + date() + ")"
    if len(title) > 90:
        title = title[0:90]
    tags.append(message.tag)
    tags.append(translate(message.tag))
    tags.extend(base)
    desc = message.desc
    clickButton('youtube\\上传', 2)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeChinese(title)
    typeTab()
    typeChinese(desc)
    typeTab()
    for i in tags:
        typeChinese(i)
        typeEnter()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeEnter()


    clickButton('youtube\\发布', 20)
    click(1, 1)


def set_good_network():
    work = False
    count = 1
    while not work and count <= 3:
        if count == 1:
            movePoint('start')
            moveRel(400, 0, 1)
            click(1, 1)
        lauch_chrome()
        movePoint('page_start')
        moveRel(150, 0, 1)
        click(1, 30)
        data = 'resource\\button\\youtube\\上传.png'
        try:
            print(now(), "尝试寻找" + data)
            pyautogui.locateCenterOnScreen(data, grayscale=True)
            return True
        except TypeError:
            print(now(), "寻找" + data + "失败, 切换服务器。")
            movePoint('ss')
            rightClick()
            moveRel(0, -200, 1)
            moveRel(-400, 0, 1)
            moveRel(-400, 0, 1)
            moveRel(0, -20 * count, 1)
            click(1, 1)
            count = count + 1
    return work





if __name__ == "__main__":
    pause(4)
    position()
