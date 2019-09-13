from spider.util.util import now, clickButton, moveRel, click, typeChinese, typeWords, typeTab, typeEnter, scroll


def upload_to_bilibili(kuaishou, douyin):
    print(now(), '开始上传快手到bilibili...')
    lauch_chrome()
    for m in kuaishou:
        print(now(), '开始上传快手' + m.title + '到bilibili...')
        upload_single_file_to_bilibili(m)
        print(now(), '成功上传快手' + m.title + '到bilibili...')

    print(now(), '开始上传抖音到bilibili...')

    return
def upload_to_youtube(kuaishou_english, douyin_english):
    print(now(), '开始上传快手_英语到youtube...')
    print(now(), '开始上传抖音_英语到youtube...')

    return

def lauch_chrome():
    clickButton('Android\\开始定位', 1)
    moveRel(400, 0, 1)
    click(1, 1)


def upload_single_file_to_bilibili(message):
    clickButton('bilibili\\bilibili', 2)
    clickButton('bilibili\\投稿', 2)
    path = message.location
    title = message.title
    tag = message.tag
    decs = message.desc
    clickButton('bilibili\\上传视频', 2)
    click(1, 1)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    clickButton('bilibili\\使用投稿模板', 2)
    clickButton('bilibili\\默认模板', 2)
    typeTab()
    typeTab()
    typeChinese("快手:" + title)
    typeTab()
    typeChinese(tag)
    typeEnter()
    typeTab()
    typeChinese(decs)
    scroll(-700)
    moveRel(-550, 350, 2)
    click(1, 120)