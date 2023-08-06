# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：unzip.py

import zipfile
import os
import sys


def get_home_path():
    env_vars = os.environ
    for var in env_vars:
        if var == "USERPROFILE" if sys.platform == "win32" else "HOME":
            return env_vars[var]


def unzip(source_path, target_path):
    with zipfile.ZipFile(source_path, 'r') as zip_ref:
        zip_ref.extractall(target_path)
    for root, dirs, files in os.walk(target_path):
        for file in files:
            os.chmod(os.path.join(root, file), 0o755)


if __name__ == '__main__':
    get_home_path()
