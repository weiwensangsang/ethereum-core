class Video():

    def __init__(self, id, caption, url, createTime, keyword, page):
        self.id = id
        self.caption = caption.replace('\n', ' ').replace(' ', '_')
        self.url = url
        self.page = page
        self.keyword = keyword
        self.createTime = createTime

    def info(self):
        return str(self.id) + " " + self.url + " " + self.caption
