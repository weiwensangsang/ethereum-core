import util


class Message:
    def __init__(self, type, location, title, tag, desc):
        self.type = type
        self.location = location
        if self.type == 'English':
            self.desc = util.translate(desc)
            self.tag = util.translate(tag)
            self.title = util.translate(title)
        elif self.type == 'Chinese':
            self.desc = desc
            self.tag = tag
            self.title = title
