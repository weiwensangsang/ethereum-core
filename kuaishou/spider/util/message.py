from spider.util.util import translate
import os

class Message:
    def __init__(self, type, location, title, tag, desc):
        self.type = type
        self.location = location.replace("..", os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
        if self.type == 'English':
            self.desc = translate(desc)
            self.tag = translate(tag)
            self.title = translate(title)
        elif self.type == 'Chinese':
            self.desc = desc
            self.tag = tag
            self.title = title
