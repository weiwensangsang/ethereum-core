import os

import requests


def test_connection():
    proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }
    r = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCRr2dbgMHtMq9Z9lbG6GqWA&key=AIzaSyAEfdBhr2EY2z1I7newyVwqFksWjMDjdTY",
        proxies=proxies)
    print(r.content)


def upload_video_to_youtube():
    proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }
    r = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos?part=snippet&id=UCRr2dbgMHtMq9Z9lbG6GqWA&key=AIzaSyAEfdBhr2EY2z1I7newyVwqFksWjMDjdTY",
        proxies=proxies)
    print(r.content)


if __name__ == "__main__":
    test_connection()
