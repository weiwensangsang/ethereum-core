import os

import requests


if __name__ == "__main__":
    r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCRr2dbgMHtMq9Z9lbG6GqWA&key=AIzaSyAEfdBhr2EY2z1I7newyVwqFksWjMDjdTY")
    print(r.content)