class Video:

    def __init__(self, id, caption, url, createTime, keyword, page):
        trans = str.maketrans("<>/\\|:\"*?", "         ")
        self.path_name = ""
        self.id = id
        self.caption = caption.replace('\n', ' ').translate(trans).replace(' ', '_')
        self.url = url
        self.page = page
        self.keyword = keyword
        self.createTime = createTime

    def info(self):
        return self.caption


