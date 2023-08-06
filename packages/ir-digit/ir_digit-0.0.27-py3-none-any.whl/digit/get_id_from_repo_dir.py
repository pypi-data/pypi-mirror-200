import os

from .load_setting import load_setting

"""
根据目录中的repo_id在本地自动获取digit_id
"""
def get_id_from_repo_dir():
    # 1. 扫描download_repo文件夹下的所有文件夹
    SETTING = load_setting()
    base_path = SETTING['base_path'].strip(".").strip("/")
    if not os.path.exists(base_path):
        return "download_repo文件夹不存在"
    resource = os.listdir(base_path)
    # 2. 查找其文件夹名字，根据repo_digit_id规则拆分出digit_id
    digit_ids = []
    for r in resource:
        if r.startswith("repo_"):
            digit_ids.append(r.split("_")[1])
    # 3. 如果有多个digit_id，返回“download_repo下有多个资源，请指定资源digit_id”
    if len(digit_ids) > 1:
        return "download_repo下有多个资源，请指定资源digit_id后重试"
    # 4. 如果没有digit_id，返回“download_repo下没有资源，请先下载资源”
    elif len(digit_ids) == 0:
        return "download_repo下没有资源，请使用 def download_repo() 下载资源"
    # 5. 如果只有一个digit_id，返回该digit_id
    else:
        return digit_ids[0]

