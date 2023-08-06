"""
base_data.py
其中包含BaseData类，用于存储数据
"""
import json
import os
from .get_id_from_repo_dir import get_id_from_repo_dir


class BaseData(object):
    def __init__(self, id: str = "default"):
        if id == "default":
            self.id = self.auto_id()
        else:
            self.id = id
        self.config = self.load_config()
        self.data = self.load_data()

    def auto_id(self):
        """
        自动找到 id
        """
        id = get_id_from_repo_dir()
        return id

    def load_config(self):
        """
        加载配置文件
        """

        config_path = f"./download_repo/repo_{self.id}/config.json"
        if not os.path.exists(config_path):
            return f"配置文件不存在，请检查路径：{config_path}"
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def data_guide(self):
        """
        数据使用说明,包括数据集说明和代码说明
        默认使用config.json中的description字段
        可自行重构方法
        """
        data_description = self.config['dataset']['description']
        code_description = self.config['code']['description']
        print(f"dataset instruction：\n{data_description}\n，code instruction：\n{code_description}")
        return {"data_description": data_description, "code_description": code_description}

    def data_scale(self):
        """
        数据规模，默认使用config.json中的data_files字段
        可自行重构方法
        """
        records = self.config['dataset']['data_files']
        for record in records:
            print(f"dataset name: {record['file_name']}\t records: {record['records']}\t size: {record['size']}")

    def load_data(self):
        """
        !!! 必须重构方法
        加载数据
        可自行重构方法
        :return : dataset
        """

        pass

    def data_preview(self):
        """
        数据预览
        """
        pass

    def data_statistics(self):
        """
        描述性统计
        """
        pass

    def data_distribution(self):
        """
        数据分布
        """
        pass

    def data_preprocessing(self):
        """
        数据预处理
        """
        pass
