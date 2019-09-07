from moviepy.editor import *

from util.util import time


class Video():

    def __init__(self, id, caption, url, createTime, keyword, page):
        self.path_name = ""
        self.id = id
        self.caption = caption.replace('\n', ' ').replace(' ', '_')
        self.url = url
        self.page = page
        self.keyword = keyword
        self.createTime = createTime

    def info(self):
        return str(self.id) + " " + self.caption


def concatenate(videos):
    print(time(), "开始视频处理...")
    vfc_list = []
    for item in videos:
        vfc = VideoFileClip(item.path_name)  # path为输入视频路径
        vfc_list.append(vfc)
    final_clip = concatenate_videoclips(vfc_list, method='compose')  # vfc_list为VideoFileClip的对象组成的list
    final_clip.write_videofile(get_sum_name(videos[0].path_name))
    print(time(), "视频合成成功")


def get_sum_name(name):
    index = name.rfind('\\')
    path = name[0: index]
    file_name = path[path.rfind('\\'): len(path)]
    return path + '\\' + file_name + '.mp4'