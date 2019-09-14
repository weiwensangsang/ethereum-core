from spider.util.util import now, clickButton, moveRel, click, typeChinese, typeTab, typeEnter, scroll, \
    movePoint, middleClick, translate


def upload_to_bilibili(kuaishou, douyin):
    print(now(), '开始上传快手到bilibili...')
    for m in kuaishou:
        lauch_chrome()
        upload_single_file_to_bilibili(m, "快手")

    print(now(), '开始上传抖音到bilibili...')
    for m in douyin:
        lauch_chrome()
        upload_single_file_to_bilibili(m, "抖音")
    return


def upload_to_youtube(kuaishou, douyin):
    print(now(), '开始设置网络...')
    set_good_network()
    print(now(), '开始上传快手到youtube...')
    for m in kuaishou:
        lauch_chrome()
        upload_single_file_to_youtube(m, "快手")
    print(now(), '开始上传抖音到youtube...')
    for m in douyin:
        lauch_chrome()
        upload_single_file_to_youtube(m, "抖音")

    return


def lauch_chrome():
    movePoint('start')
    moveRel(350, 0, 1)
    middleClick()


def upload_single_file_to_bilibili(message, type):
    movePoint('page_start')
    click(1, 1)
    path = message.location
    title = message.title
    tag = message.tag
    decs = message.desc
    movePoint('bilibili_upload_video')
    click(2, 1)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    clickButton('bilibili\\使用投稿模板', 2)
    clickButton('bilibili\\默认模板', 2)
    typeTab()
    typeTab()
    typeChinese(type + ": " + title)
    typeTab()
    typeChinese(tag)
    typeEnter()
    typeTab()
    typeChinese(decs)
    scroll(-700)
    moveRel(-550, 350, 2)
    click(1, 1)


def upload_single_file_to_youtube(message, type):
    tags = ['抖音', '快手', 'Tik Tok', 'kuaishou']
    movePoint('page_start')
    moveRel(150, 0, 1)
    click(1, 5)
    path = message.location
    title = message.title + " " + translate(message.title)
    tags.append(message.tag)
    tags.append(translate(message.tag))
    decs = message.decs
    clickButton('youtube\\选取要上传的视频', 2)
    typeChinese(path)
    clickButton('bilibili\\确定', 2)
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeTab()
    typeChinese(type + ": " + title)
    typeTab()
    typeChinese(decs)
    typeTab()
    for i in tags:
        typeChinese(i)
        typeEnter()
    clickButton('youtube\\发布', 2)

def set_good_network():
    return

if __name__ == "__main__":
    lauch_chrome()
    upload_single_file_to_youtube('', 'kuaishou', '0')
