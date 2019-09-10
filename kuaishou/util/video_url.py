import hashlib

import requests

from util.util import now
from util.video import Video


def get_video_url(keyword, page):
    print(now(), '抓取关键字:"' + keyword + '", 抓取页数:' + page)
    print(now(), '开始构造签名...')
    params = {
        'isp': 'CMCC',
        'mod': 'oppo(a37f)',
        'lon': '116.41025',
        'country_code': 'cn',
        'kpf': 'ANDROID_PHONE',
        'did': 'ANDROID_4a9ac991b99dc1a3',
        'kpn': 'KUAISHOU',
        'net': 'WIFI',
        'app': '0',
        'oc': 'MYAPP,1',
        'ud': '1487941148',
        'hotfix_ver': '',
        'c': 'MYAPP,1',
        'sys': 'ANDROID_5.1.1',
        'appver': '6.1.0.8039',
        'ftt': '',
        'language': 'zh-cn',
        'iuid': '',
        'lat': '39.916411',
        'did_gt': '1567786260360',
        'ver': '6.1',
        'max_memory': '192',
        'keyword': keyword,
        'fromPage': page,
        'client_key': '3c2cd3f3',
        '__NStokensig': 'xiazhen',
        'token': '06838c45daaa4613af222815af9f2d23-1487941148',
        'os': 'android'
    }
    if int(page) > 0:
        params.update({'pcursor': page})
    sig = get_sig(params)
    params.update({'sig': sig})
    print(now(), '签名构造成功，开始数据抓取...')
    r = requests.post("http://api.gifshow.com/rest/n/search", params=params)
    print(now(), '数据抓取成功，开始视频链接解析...')
    result = []
    for item in r.json().get('feeds'):
        if 'main_mv_urls' in item.keys():
            v = Video(item.get('photo_id'), item.get('caption'),
                      item.get('main_mv_urls')[0].get('url'), item.get('time'), keyword, page)
            result.append(v)
    return result


def get_sig(param, salt='382700b563f4'):
    param.pop('__NStokensig')
    keys = list(param.keys())
    keys.sort()
    temp_str = ''
    for key in keys:
        temp_str = temp_str + key + '=' + param[key]
    sig = temp_str + salt
    m = hashlib.md5()
    m.update(sig.encode(encoding='utf-8'))
    str_md5 = m.hexdigest()
    return str_md5
