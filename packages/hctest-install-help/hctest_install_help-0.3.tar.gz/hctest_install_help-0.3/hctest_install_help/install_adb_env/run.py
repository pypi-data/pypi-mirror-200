# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：run.py

import ctypes
import sys


def run_cmd_as_admin(cmd):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/k {}".format(cmd), None, 1)
    else:
        import subprocess
        subprocess.Popen(cmd, shell=True)


if sys.platform == "win32":
    env_file = str(__file__).replace(f"run.py", "adb_env.py")
    run_cmd_as_admin(f"{sys.executable} {env_file}")

else:

    env_file = str(__file__).replace(f"run.py", "adb_env.py")
    import os

    # sudo_password = input("请输入你的系统管理员的账户密码：")
    # os.system(f'echo "{sudo_password}" | sudo -S {sys.executable} {env_file}')

    import os
    import subprocess

    if os.geteuid() == 0:
        # print("当前进程以管理员权限运行。")
        subprocess.Popen(f'{sys.executable} {env_file}')
    else:
        print(f"sudo {sys.executable} {env_file}")
        # command = ["sudo", f"{sys.executable}", f"{env_file}"]
        # subprocess.run(command, check=True)

        command = ["sudo", "-S", f"{sys.executable}", f"{env_file}"]

        subprocess.run(command, check=True, input='986897\n', encoding='utf-8')
