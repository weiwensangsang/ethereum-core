import sys
import os

from spider.util.message import Message

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from moviepy.editor import *

from spider.util.util import now





def concatenate(vm):
    videos = vm.data
    print(now(), "开始视频处理...")
    vfc_list = []
    for item in videos:
        vfc = VideoFileClip(item.path_name)  # path为输入视频路径
        vfc_list.append(vfc)
    final_clip = concatenate_videoclips(vfc_list, method='compose')  # vfc_list为VideoFileClip的对象组成的list
    location = get_sum_name(videos[0].path_name)
    final_clip.write_videofile(location)
    print(now(), "视频合成成功，开始进行工作区清理...")
    clean_workspace(videos[0].path_name)
    print(now(), "工作区清理成功，开始生成上传数据...")
    return Message('Chinese', location, vm.title, vm.tag, vm.decs)


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
    print(now(), "工作区清理成功，本次视频处理完成。")
