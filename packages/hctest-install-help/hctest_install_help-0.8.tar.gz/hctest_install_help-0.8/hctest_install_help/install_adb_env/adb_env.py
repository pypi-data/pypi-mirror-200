# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：adb_env.py

from hctest_install_help.package.unzip import *

ANDROID_HOME_NAME = "ANDROID_HOME"
JAVA_HOME_NAME = "JAVA_HOME"
adb_path = None
aapt_path = None
adb_zip_file = input("请输入你adb源文件(zip文件)绝对路径:\n")
aapt_zip_file = input("请输入你的appt源文件(zip文件)绝对路径:\n")
save_path = input("请输入你想保存的位置(文件夹的绝对路径):\n")

if not save_path:
    home = get_home_path()
    target_path = os.path.abspath(home + r"\SDK" if sys.platform == "win32" else home + r"/.SDK")
    unzip(adb_zip_file, target_path)
    unzip(aapt_zip_file, target_path)

else:
    target_path = os.path.abspath(save_path)
    unzip(adb_zip_file, target_path)
    unzip(aapt_zip_file, target_path)

for dir_path, dir_names, filenames in os.walk(target_path):
    for filename in filenames:
        if filename.endswith("adb.exe" if sys.platform == "win32" else "adb"):
            adb_path = os.path.join(dir_path)

for dir_path, dir_names, filenames in os.walk(target_path):
    for filename in filenames:
        if filename.endswith("aapt.exe" if sys.platform == "win32" else "aapt"):
            aapt_path = os.path.join(dir_path)

if sys.platform == "win32":
    from hctest_install_help.package.windows_env import *
    import subprocess

    add_system_env_path(r"%ANDROID_HOME%{};%ANDROID_HOME%{}".format(aapt_path.replace(target_path, ''),
                                                                    adb_path.replace(target_path, '')))
    add_system_env(ANDROID_HOME_NAME, target_path)
    subprocess.call(["attrib", "+h", target_path])

else:
    from hctest_install_help.package.mac_env import *

    add_system_env_path(r"$ANDROID_HOME{}:$ANDROID_HOME{}".format(aapt_path.replace(target_path, ''),
                                                                  adb_path.replace(target_path, '')))
    add_system_env(ANDROID_HOME_NAME, target_path)
