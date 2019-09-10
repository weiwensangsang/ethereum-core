import math
import time

import requests


def douyin():
    TIMESTAMP = str(math.floor(time.time() * 1000))

    print(TIMESTAMP[:-3])
    print(TIMESTAMP)
    headers = {
        "Host": "aweme-hl.snssdk.com",
        "Connection": "keep-alive",
        "Content-Length": "154",
        "Cookie": "install_id=85825016768; ttreq=1$67ccaed509ecbd3f3f91e9fd46a277ccf495e30b; odin_tt=2735e1d379b5e2cabeb7441660e064f137c5ffb4721d91519175aac1074de14f884dd0f0ac4f4de90189b0033b0f7d1636022b7e7e3528607d68ae25e9421469; sid_guard=71c4591035e0bc3f4dc3a5ee6640c351%7C1568129672%7C5184000%7CSat%2C+09-Nov-2019+15%3A34%3A32+GMT; uid_tt=198d816e792ace6183f544c3e71e8425; sid_tt=71c4591035e0bc3f4dc3a5ee6640c351; sessionid=71c4591035e0bc3f4dc3a5ee6640c351",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": "1568135111269",
        "X-Tt-Token": "0071c4591035e0bc3f4dc3a5ee6640c351c78756bd630f9376e7b33227aa7650e17e7d09cda9f610de90c876bf3c265a5b4f",
        "sdk-version": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-SS-STUB": "B3C4479470A8B45C25444911293BCA41",
        "x-tt-trace-id": "00-2639e24b32c0ec80ac455a84eff03901-2639e24b32c0ec80-01",
        "User-Agent": "com.ss.android.ugc.aweme/790 (Linux; U; Android 5.1.1; zh_CN; HUAWEI MLA-AL10; Build/HUAWEIMLA-AL10; Cronet/58.0.2991.0)",
        "X-Gorgon": "0300dc76400140e9c8bcb13becf7d3fc23bab92be2e537241ab7",
        "X-Khronos": "1568135111"
    }
    url = 'http://aweme-hl.snssdk.com/aweme/v1/search/item/'
    params = {
        'os_api': '22',
        'device_type': 'HUAWEI MLA-AL10',
        'ssmix': 'a',
        'manifest_version_code': '790',
        'dpi': '320',
        'js_sdk_version': '1.25.0.1',
        'uuid': '863064010101238',
        'app_name': 'aweme',
        'version_name': '7.9.0',
        'ts': TIMESTAMP[:-3],
        'app_type': 'normal',
        'ac': 'wifi',
        'update_version_code': '7902',
        'channel': 'tengxun_new',
        '_rticket': TIMESTAMP,
        'device_platform': 'android',
        'iid': '85825016768',
        'version_code': '790',
        'openudid': '107b447da6f13132',
        'device_id': '68895521699',
        'resolution': '900*1600',
        'os_version': '5.1.1',
        'language': 'zh',
        'device_brand': 'HUAWEI',
        'aid': '1128',
        'mcc_mnc': '46007'
    }

    body = {
        "keyword": "美女收藏家",
        "offset": "0",
        "count": "10",
        "source": "video_search",
        "is_pull_refresh": "1",
        "hot_search": "0",
        "search_id": "",
        "query_correct_type": "1"
    }
    r = requests.post(url, headers=headers, params=params, data=body)
    print(r.text)


if __name__ == "__main__":
    douyin()
