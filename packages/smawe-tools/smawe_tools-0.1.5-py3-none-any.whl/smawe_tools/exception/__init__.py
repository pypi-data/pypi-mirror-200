# -*- coding: utf-8 -*-
# @Author  : Smawe
# @Time    : 2023/3/25 14:27
# @File    : __init__.py.py
# @Software: PyCharm
class MaxRetryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
