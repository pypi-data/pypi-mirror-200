# -*- coding: utf-8 -*-
# @Author  : Smawe
# @Time    : 2023/1/17 19:11
# @File    : setup.py
# @Software: PyCharm

from setuptools import find_packages, setup
from smawe_tools import version


with open("README.md", "r", encoding="utf-8") as fp:
    LONG_DESCRIPTION = fp.read()

NAME = 'smawe_tools'
DESCRIPTION = 'small tool'
EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.5.0'

about = {"__version__": version}


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=('tests',)),
    install_requires=['retrying', 'colorama'],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
