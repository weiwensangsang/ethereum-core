from spider.util.util import now, clickButton, moveRel, click, typeChinese, typeWords, typeTab, typeEnter, scroll


def upload_to_bilibili(kuaishou, douyin):
    print(now(), '开始上传快手到bilibili...')
    lauch_bilibili()
    #for item in kuaishou:
    path = "C:\\Users\\weiwensangsang\\Documents\\GitHub\\WeBattle\\kuaishou\\resource\\kuaishou\\2019-09-13_长腿\\2019-09-13_长腿.mp4"
    title = '2019-09-13 快手大长腿'
    tag = '长腿'
    decs = '快手大长腿'
    clickButton('bilibili\\上传视频', 2)
    click(1, 1)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    clickButton('bilibili\\使用投稿模板', 2)
    clickButton('bilibili\\默认模板', 2)
    typeTab()
    typeTab()
    typeChinese(title)
    typeTab()
    typeChinese(tag)
    typeEnter()
    typeTab()
    typeChinese(decs)
    scroll(-700)
    moveRel(-550, 350, 2)
    click(1, 60)
    #clickButton('bilibili\\立即投稿', 2)

    print(now(), '开始上传抖音到bilibili...')

    return
def upload_to_youtube(kuaishou_english, douyin_english):
    print(now(), '开始上传快手_英语到youtube...')
    print(now(), '开始上传抖音_英语到youtube...')

    return

def lauch_bilibili():
    clickButton('Android\\开始定位', 1)
    moveRel(400, 0, 1)
    click(1, 1)
    clickButton('bilibili\\bilibili', 2)
    clickButton('bilibili\\投稿', 2)
