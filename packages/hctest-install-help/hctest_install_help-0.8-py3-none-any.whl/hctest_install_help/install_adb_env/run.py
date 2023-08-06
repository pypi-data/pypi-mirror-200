# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：run.py

import ctypes
import sys


def run_cmd_as_admin(cmd):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/k {}".format(cmd), None, 1)
    else:
        import os
        os.system(cmd)


def start_install_help():
    if sys.platform == "win32":
        env_file = str(__file__).replace(f"run.py", "adb_env.py")
        run_cmd_as_admin(f"{sys.executable} {env_file}")

    else:
        import os
        env_file = str(__file__).replace(f"run.py", "adb_env.py")
        os.system(f'{sys.executable} {env_file}')
