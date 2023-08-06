import json

from .load_setting import load_setting

"""
加载配置文件
"""


def load_config(id):
    """
    加载数据对应的config.json配置文件
    :param: id 数据id
    :return: dict 返回config.json文件的内容
    """
    SETTING = load_setting()
    with open(f'{SETTING["base_path"]}repo_{id}/config.json', 'r', encoding='UTF-8') as f:
        return json.load(f)
