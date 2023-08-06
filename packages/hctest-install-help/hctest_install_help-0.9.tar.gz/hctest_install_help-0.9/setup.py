# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：setup.py
from setuptools import setup, find_packages

setup(
    name="hctest_install_help",
    version="0.9",
    description="辅助帮你下载安装文件",
    author="cf",
    author_email="dingjun_baby@yeah.net",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    # install_requires=[
    #     'requests',
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

