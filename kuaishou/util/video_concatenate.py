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
        return self.caption


def concatenate(videos):
    print(time(), "开始视频处理...")
    vfc_list = []
    for item in videos:
        vfc = VideoFileClip(item.path_name)  # path为输入视频路径
        vfc_list.append(vfc)
    final_clip = concatenate_videoclips(vfc_list, method='compose')  # vfc_list为VideoFileClip的对象组成的list
    final_clip.write_videofile(get_sum_name(videos[0].path_name))
    print(time(), "视频合成成功，开始进行工作区清理...")
    clean_workspace(videos[0].path_name)


def get_sum_name(name):
    index = name.rfind('\\')
    path = name[0: index]
    file_name = path[path.rfind('\\'): len(path)]
    return path + '\\' + file_name + '.mp4'


def get_sum_path(name):
    return name[0: name.rfind('\\')] + '\\'


def clean_workspace(name):
    for f in os.listdir(get_sum_path(name)):
        if not f.startswith('20'):
            file = os.path.join(get_sum_path(name), f)
            if os.path.isfile(file):
                os.remove(file)
    print(time(), "工作区清理成功，本次视频处理完成。")
