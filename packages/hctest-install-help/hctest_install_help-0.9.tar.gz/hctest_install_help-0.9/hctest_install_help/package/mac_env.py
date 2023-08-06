# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：mac_env.py

import subprocess


def add_system_env_path(path_):
    cmd = f"echo export 'PATH={path_}:$PATH.' >> ~/.bash_profile"
    subprocess.call(cmd, shell=True)


def add_system_env(env_name, env_value):
    cmd = f"echo export '{env_name}={env_value}' >> ~/.bash_profile"
    subprocess.call(cmd, shell=True)
