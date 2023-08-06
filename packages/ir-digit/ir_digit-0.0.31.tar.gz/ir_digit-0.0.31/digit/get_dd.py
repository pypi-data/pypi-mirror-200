import inspect
import os
import sys

from .get_id_from_repo_dir import get_id_from_repo_dir
from .load_setting import load_setting


def get_dd(id: str = 'default'):
    SETTING = load_setting()
    base_path = SETTING['base_path'].strip(".").strip("/")
    if id == 'default':
        id = get_id_from_repo_dir()

    sec_path = f'repo_{id}'
    imp_module = f'repo_{id}'
    imp_class = 'DigitData'
    if not os.path.exists(f"./{base_path}/{sec_path}"):
        return f"资源{sec_path}不存在，请先下载资源"

    if not os.path.exists(f"./{base_path}/{sec_path}/code.py"):
        return f"资源{sec_path}中缺少code.py文件,请更新资源"

    if not os.path.exists(f"./{base_path}/{sec_path}/__init__.py"):
        # 创建__init__.py文件
        with open(f"./{base_path}/{sec_path}/__init__.py", 'w', encoding='utf-8') as f:
            f.write("")
    # 添加路径，加载code.py文件，
    sys.path.append(f"./{base_path}")

    ip_module = __import__(f"{imp_module}.code", fromlist=['code'])
    clss = inspect.getmembers(ip_module, inspect.isclass)
    # 判断DigitData类是否存在
    for cls in clss:
        if cls[0] == imp_class:
            if inspect.getmro(cls[1])[1].__name__ in ['TableData', 'LabelData', 'DocData', 'ImageData', 'AudioData',
                                                      'VideoData', 'GraphData']:
                break
            else:
                return "DigitData类不是规定类 TableData, LabelData, DocData, ImageData, AudioData, VideoData, GraphData 的子类"
        else:
            return "DigitData类不存在"
    # 加载DIgitData类
    DD = getattr(ip_module, imp_class)  # 获取类
    return DD()  # 实例化类并返回
