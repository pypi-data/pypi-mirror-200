import requests

from ..load_setting import load_setting


def get_new_id():
    """
    获取新的id,使用华为云服务器，GET请求
    :return:id:str
    """
    # url = "http://
    SETTING = load_setting()
    url = SETTING['url']['HuaweiCould Interface'] + 'new_id/'
    # 线上运行url
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'normal':
        return data['data_id']
    else:
        return "函数get_new_id出现错误，请检查网络接口是否正常"
