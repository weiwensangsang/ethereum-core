import math
import time
import json
import requests
from selenium import webdriver


def douyin():
    driver = webdriver.Chrome()
    str_file = '1.json'
    with open(str_file, 'r', encoding='utf-8') as f:
        print("Load str file from {}".format(str_file))
        s = f.read()
    data_json = json.loads(s)
    urls = []
    for item in data_json.get('aweme_list'):
        print(item.get('share_info').get('share_link_desc'))
        s = item.get('share_info').get('share_url')
        # print(s)
        driver.get(s)  # 加载网页
        data = driver.page_source  # 获取网页文本
        url = data[(data.find('playAddr') + 11): data.find('cover')].split('\"')[0]
        driver.get(url)
        print(driver.current_url)
        urls.append(url)
    driver.quit()


if __name__ == "__main__":
    douyin()

    # r = requests.get(
    #     'http://ddcb0660.tt.x.bsgslb.cn/xdispatch72f84b52da078f20/v9-dy-y.ixigua.com/2ff4b4be64083e52ffa3fa35a7252849/5d791f6f/video/m/22037509c051c414d70bdff38e2fe220a4411637847b00000b529a048eac/?a=1128&br=1354&cr=0&cs=0&dr=0&ds=3&er=&l=20190911232241010156035154905E65&lr=aweme&rc=andkdWpvajs2bzMzZ2kzM0ApZzc8O2c6OjxmN2Y2ZzozZWdhXmxvLWVsMG9fLS0wLS9zczJiMF4uMDEwXmM0LS82NWM6Yw%3D%3D&bsxdisp=co',
    #     stream=True)
    # _name = "1.mp4";
    # with open(_name, "wb") as mp4:
    #     for chunk in r.iter_content(chunk_size=1024 * 1024):
    #         if chunk:
    #             mp4.write(chunk)
