"""
base_data.py
其中包含BaseData类，用于存储数据
"""
import json
import os


class BaseData(object):
    def __init__(self, digit_id: str = "default"):
        if digit_id == "default":
            self.digit_id = self.auto_digit_id()
        else:
            self.digit_id = digit_id
        self.config = self.load_config()
        self.data = self.load_data()

    def auto_digit_id(self):
        """
        自动找到 digit_id
        """
        # 1. 扫描download_repo文件夹下的所有文件夹
        base_path = "./download_repo"
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

    def load_config(self):
        """
        加载配置文件
        """

        config_path = f"./download_repo/repo_{self.digit_id}/config.json"
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
