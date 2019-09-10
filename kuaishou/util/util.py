import datetime
import hashlib
import urllib
import random
import requests
import time
import pyautogui


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


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')


def file_time():
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


def type(data, t):
    print(now(), "键盘输入:" + data)
    pyautogui.typewrite(data, t)  # 0.25表示每输完一个字符串延时0.25秒


def typeEnter():
    print(now(), "键盘输入:回车")
    pyautogui.typewrite(['enter'], 0.1)  # 0.25表示每输完一个字符串延时0.25秒


def clickPic(data):
    if data == 'start':
        png ='png/1.png'
    elif data == '2':
        png = 'png/3.png'



    try:
        print(now(), "寻找" + data + "按钮:" + png)
        corn_locate = pyautogui.locateOnScreen(png)  # 找到按钮所在坐标，分别含义是按钮左上角x坐标，左上角y坐标，x方向大小，y方向大小 (5, 560, 54, 54)
        corn_center_x, corn_center_y = pyautogui.center(corn_locate)  # 找到按钮中心点
    except TypeError :
        print(now(), "寻找" + data + "按钮失败")
    else:
        print(now(), "点击" + data + "按钮")
        pyautogui.click(corn_center_x, corn_center_y)  # 点击按钮


if __name__ == "__main__":
    clickPic('2')
