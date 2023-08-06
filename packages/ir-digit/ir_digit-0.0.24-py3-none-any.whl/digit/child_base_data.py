# -*- coding:utf-8 -*-

from .base_data import BaseData

"""
按照下面的继承关系实现各个数据类
- BaseData
    - RelationalData
        - TableData
        - LabelData
    - NonRelationalData
        - DocData
        - PhotoData
        - VideoData
        - AudioData
    - GraphData
"""


class RelationalData(BaseData):
    """
    关系型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class TableData(RelationalData):
    """
    表格型数据类,集成继承关系型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class LabelData(RelationalData):
    """
    标签型数据类，继承关系型数据类s
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class NonRelationalData(BaseData):
    """
    非关系型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class DocData(NonRelationalData):
    """
    文本型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class ImageData(NonRelationalData):
    """
    图片型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class VideoData(NonRelationalData):
    """
    视频型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class AudioData(NonRelationalData):
    """
    音频型数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)


class GraphData(BaseData):
    """
    图数据类
    """

    def __init__(self, id: str = "defeat"):
        super().__init__(id)
