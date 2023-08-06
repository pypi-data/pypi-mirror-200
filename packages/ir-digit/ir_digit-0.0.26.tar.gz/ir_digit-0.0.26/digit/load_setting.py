import json
import sys
import os
"""
加载设置文件
"""


def load_setting():
    # 先获取当前运行时临时目录路径
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)

    # 使用 os.path.join() 方法，将 临时目录路径与文件相对路径拼接
    with open(os.path.join(basedir, 'setting.json'), 'r', encoding='UTF-8') as f:
        return json.load(f)



