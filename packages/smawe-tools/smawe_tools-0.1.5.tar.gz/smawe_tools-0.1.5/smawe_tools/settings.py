# -*- coding: utf-8 -*-
# @Author  : Smawe
# @Time    : 2023/3/25 14:45
# @File    : settings.py
# @Software: PyCharm
import logging
import platform
try:
    from colorama import init as _init
    _init(autoreset=True)
except ModuleNotFoundError:
    pass

# 进行日志配置，后续会使用到
logging.basicConfig(format="%(asctime)s:%(filename)s:%(threadName)s:%(levelname)s:%(message)s", level=logging.INFO)

_IS_LESS_THEN_PY39 = float(".".join(platform.python_version_tuple()[:-1])) < 3.9
if _IS_LESS_THEN_PY39:
    import typing
    List = typing.List
else:
    List = list

# 'Linux', 'Darwin', 'Java', 'Windows'
OS_NAME = platform.system()


def modify_encoding(encoding="utf-8", language_code="en_US"):
    import _locale
    _locale._getdefaultlocale = lambda *args, **kwargs: (language_code, encoding)
