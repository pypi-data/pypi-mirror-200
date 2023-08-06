import sys

from .load_setting import load_setting
from .get_id_from_repo_dir import get_id_from_repo_dir


def get_dd(id:str = 'default'):
    SETTING = load_setting()
    base_path = SETTING['base_path'].strip(".").strip("/")
    if id == 'default':
        id = get_id_from_repo_dir()

    sec_path = f'repo_{id}'
    sys.path.append(f"./{base_path}/{sec_path}")
    dd = __import__(f"{base_path}.{sec_path}.code.DigitData")
    return dd
