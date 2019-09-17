import datetime
import hashlib
import os
import random
import time
import urllib

import pyautogui
import pyperclip
import requests
import shutil


def translate(message):
    appid = '20190910000333359'  # 你的appid
    secretKey = 'x7xTVBFeaVKx_VY8pnRQ'  # 你的密钥
    myurl = '/api/trans/vip/translate'
    q = message
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    r = requests.get('http://api.fanyi.baidu.com' + myurl)
    return r.json().get('trans_result')[0].get('dst')


def get_sum_name(name):
    index = name.rfind('\\')
    path = name[0: index]
    file_name = path[path.rfind('\\'): len(path)]
    return path + '\\' + file_name + '.mp4'


def get_sum_path(name):
    return name[0: name.rfind('\\')] + '\\'


def get_trans():
    return str.maketrans("<>/\\|:\"*?\n", "          ")


def clean_workspace(name):
    for f in os.listdir(get_sum_path(name)):
        if not f.startswith('20'):
            file = os.path.join(get_sum_path(name), f)
            if os.path.isfile(file):
                try:
                    os.remove(file)
                except PermissionError:
                    print(now(), "本文件无法删除，跳过。")
    print(now(), "工作区清理成功，本次视频处理完成。")


def clean_douyin_json():
    path = "resource\\douyin\\"
    for d in os.listdir(path):
        if not d.startswith('20'):
            path_file = os.path.join(path, d)
            for f in os.listdir(path_file):
                path_file2 = os.path.join(path_file, f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)
            os.removedirs(path_file)


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')


def date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


class VM:
    def __init__(self, data, title, tag, desc):
        self.tag = tag
        self.decs = desc
        self.title = title
        self.data = data


def pause(s):
    if s <= 0:
        return
    print(now(), "暂停 %d 秒" % s)
    time.sleep(s)


def moveTo(x, y, s):
    print(now(), "光标向屏幕绝对位置 (" + str(x) + "," + str(y) + ") 处移动, 移动时间 " + str(s) + "秒")
    pyautogui.moveTo(x=x, y=y, duration=s, tween=pyautogui.linear)


def moveRel(x, y, s):
    print(now(), "光标向相对当前光标位置 (" + str(x) + "," + str(y) + ") 处移动, 移动时间 " + str(s) + "秒")
    pyautogui.moveRel(x, y, duration=s)


def click(n, m):
    while n > 0:
        print(now(), "光标点击左键" + str(n) + "次")
        pyautogui.click(button='left')
        pause(m)
        n = n - 1


def middleClick():
    pyautogui.middleClick()


def rightClick():
    print(now(), "光标点击右键")
    pyautogui.rightClick()


def typeChinese(data):
    print(now(), "键盘输入:" + data)
    pyperclip.copy(data)
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')


def typeWords(data):
    print(now(), "键盘输入汉字:" + data)
    pyautogui.typewrite(data, 0.5)  # 0.25表示每输完一个字符串延时0.25秒


def typeEnter():
    print(now(), "键盘输入:回车")
    pyautogui.typewrite(['enter'], 0.1)  # 0.25表示每输完一个字符串延时0.25秒


def typeTab():
    print(now(), "键盘输入:TAB")
    pyautogui.typewrite(['tab'], 0.1)  # 0.25表示每输完一个字符串延时0.25秒


def clickButton(data, s):
    data = 'resource\\button\\' + data + '.png'

    try:
        print(now(), "寻找" + data)
        corn_locate = pyautogui.locateCenterOnScreen(data,
                                                     grayscale=True)  # 找到按钮所在坐标，分别含义是按钮左上角x坐标，左上角y坐标，x方向大小，y方向大小 (5, 560, 54, 54)
    except TypeError:
        print(now(), "寻找" + data + "失败")
    else:
        print(now(), "点击" + data)
        pyautogui.click(corn_locate)  # 点击按钮
        pause(s)


def rightClickButton(data, s):
    data = 'resource\\button\\' + data + '.png'

    try:
        print(now(), "寻找" + data)
        corn_locate = pyautogui.locateCenterOnScreen(data,
                                                     grayscale=True)  # 找到按钮所在坐标，分别含义是按钮左上角x坐标，左上角y坐标，x方向大小，y方向大小 (5, 560, 54, 54)
    except TypeError:
        print(now(), "寻找" + data + "失败")
    else:
        print(now(), "右键点击" + data)
        pyautogui.rightClick(corn_locate)  # 点击按钮
        pause(s)


def drag(len, duration):
    pyautogui.dragRel(0, 0 - len, duration=duration)
    pause(5)


def dragCurrent():
    print(now(), "拖拽" + str(len))
    moveRel(0, 300, 1)
    pyautogui.dragRel(0, -300, button='left')  # 绝对移动


def scroll(len):
    pyautogui.scroll(len)


def position():
    pos = pyautogui.position()  # 获取当前鼠标的位置
    posStr = "Position:" + str(pos.x).rjust(4) + ',' + str(pos.y).rjust(4)
    print(posStr)


def movePoint(name):
    if name == 'start':
        moveTo(200, 1050, 1)
    elif name == 'page_start':
        moveTo(165, 80, 1)
    elif name == 'bilibili_upload_video':
        moveTo(1060, 485, 1)
    elif name == 'refresh_page':
        moveTo(95, 50, 1)
    elif name == 'ss':
        moveTo(1616, 1058, 1)
    elif name == 'lock':
        moveTo(1121, 882, 1)
    elif name == 'bilibili_upload':
        moveTo(1136, 88, 1)

def clean_start_workspace(dir):
    print(now(), "清理工作区" + dir)
    path = "resource\\" + dir + "\\"
    shutil.rmtree(path)


if __name__ == "__main__":
    pause(5)
    position()
