627035101394-ggt7q1q7pm2pv47nit6hv30udhicup8k.apps.googleusercontent.com


https://developers.google.com/apis-explorer/#p/youtube/v3/

https://guozh.net/318/

pip install google-auth-oauthlib

https://developers.google.cn/youtube/v3/getting-started?hl=zh-tw

apikey 只能用作读
一定要用oauth2
如果用官方代码，就必要找到python全局代理的写法，else用request会好很多。

set http_proxy=http:127.0.0.1:1080
set https_proxy=http:127.0.0.1:1080

python util/upload.py --file="util/1.mp4" --title="Summer vacation in California" --description="Had fun surfing in Santa Cruz" --keywords="surfing,Santa Cruz" --category="22" --privacyStatus="private"

youtube-upload --email=xalyf@bupt.edu.cn --password=xzlyf159357 --title="A.S. Mutter" --description="A.S. Mutter plays Beethoven" --category=Music --keywords="mutter, beethoven" 1.mp4

youtube-upload --title="A.S. Mutter" 1.mp4