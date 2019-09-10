import datetime
import hashlib
import urllib
import random
import requests


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


def time():
    return datetime.datetime.now().strftime('%H:%M:%S')


def file_time():
    return datetime.datetime.now().strftime('%Y-%m-%d')


class VM:
    def __init__(self, data, title, tag, decs):
        self.tag = tag
        self.decs = decs
        self.title = title
        self.data = data
