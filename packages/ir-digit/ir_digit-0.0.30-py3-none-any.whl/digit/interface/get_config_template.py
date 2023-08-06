import json

import requests

from ..load_setting import load_setting


def get_config_template():
    """
    获取配置文件模板
    """
    SETTING = load_setting()
    url = f"{ SETTING['url']['HuaweiCould Interface'] }/config"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"模板文件下载失败，response.status_code = {response.status_code}")
    else:
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        print("模板文件下载完成，可在当前目录下查看./config.json")
