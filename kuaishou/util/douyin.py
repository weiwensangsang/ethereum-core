import math
import time
import json
import requests
from selenium import webdriver

def douyin():
    str_file = '1.json'
    with open(str_file, 'r', encoding='utf-8') as f:
        print("Load str file from {}".format(str_file))
        s = f.read()
    data_json = json.loads(s)
    #for item in data_json.get('aweme_list'):
        # print(item.get('share_info').get('share_link_desc'))
    s = data_json.get('aweme_list')[0].get('share_info').get('share_url')
    print(s)

    import http.client

    conn = http.client.HTTPSConnection("www.iesdouyin.com")

    headers = {
        'cache-control': "no-cache",
        'postman-token': "733f4d80-4771-b661-e40a-07a45c12d956"
    }

    conn.request("GET",
                 "/share/video/6734485326976339204/?region=CN&mid=6734476076120460043&u_code=15m95d0il55c&titleType=title",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    #print(re.content)


if __name__ == "__main__":
    #douyin()
    driver = webdriver.PhantomJS()
    driver.get('https://www.iesdouyin.com/share/video/6734485326976339204/?region=CN&mid=6734476076120460043&u_code=15m95d0il55c&titleType=title')  # 加载网页
    data = driver.page_source  # 获取网页文本
    driver.save_screenshot('1.png')  # 截图保存
    print(data)
    driver.quit()
