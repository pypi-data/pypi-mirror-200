from .load_setting import load_setting
import sys
from .load_config import load_config

def get_dd(id:str = 'default'):
    if id == 'default':
        id = load_config()['id']
    SETTING = load_setting()
    base_path = SETTING['base_path'].strip(".").strip("/")
    sec_path = f'repo_{id}'
    sys.path.append(f"{base_path}/{sec_path}")
    dd = __import__("from {base_path}.{sec_path}.code import DigitData")
    return dd





