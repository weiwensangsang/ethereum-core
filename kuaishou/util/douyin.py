import math
import time
import json
import requests
from selenium import webdriver


def douyin():
    driver = webdriver.PhantomJS()
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
        print(url)
        urls.append(url)
    driver.quit()

    driver2 = webdriver.PhantomJS()
    a = driver2.get(urls[0])
    print(a.page_source)

    # print(re.content)
    driver.quit()


if __name__ == "__main__":
    #douyin()
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = "https://www.baidu.com/"
    driver.get(url)
    time.sleep(2)
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("当前时间：", nowtime)
    print(driver.title)
    driver.quit()
    #driver.get('https://www.baidu.com')

    driver.get('https://aweme.snssdk.com/aweme/v1/play/?s_vid=93f1b41336a8b7a442dbf1c29c6bbc5631b2d3f5c98c5d9f8244065a06e0c6557773667c5dc17cdf1df5d3156df395f62270ac162a201b2accaf38c3f3e3102b&line=0')
    time.sleep(1)
    driver.save_screenshot("1.png")
    driver.switch_to.window(driver.window_handles[0])
    print(driver.current_url)
    r = requests.get(
        'http://v26-dy.ixigua.com/56242247a17e0e5bcf750cd0876f0019/5d78db56/video/m/22037509c051c414d70bdff38e2fe220a4411637847b00000b529a048eac/?a=1128&br=1354&cr=0&cs=0&dr=0&ds=3&er=&l=2019091118320801000302608400743F&lr=aweme&rc=andkdWpvajs2bzMzZ2kzM0ApZzc8O2c6OjxmN2Y2ZzozZWdhXmxvLWVsMG9fLS0wLS9zczJiMF4uMDEwXmM0LS82NWM6Yw%3D%3D',
        stream=True)
    _name = "1.mp4";
    with open(_name, "wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                mp4.write(chunk)
