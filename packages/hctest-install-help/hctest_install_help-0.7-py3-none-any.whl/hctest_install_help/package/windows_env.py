# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：windows_env.py


import winreg


def add_system_env_path(path_):
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                             0, winreg.KEY_ALL_ACCESS)
        value, type_ = winreg.QueryValueEx(key, "Path")
        if path_ not in value:
            value = value.rstrip(";")  # 去除末尾的分号
            value += ";" + path_
            winreg.SetValueEx(key, "Path", 0, type_, value)
            print(f"Successfully added {path_} to system environment variables.")
        else:
            print(f"{path_} already exists in system environment variables.")
    except WindowsError:
        print("Error occurred while trying to add path to system environment variables.")


def add_system_env(env_name, env_value):
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                             0, winreg.KEY_READ)
        try:
            value, regtype = winreg.QueryValueEx(key, env_name)
        except FileNotFoundError:
            value = None
        winreg.CloseKey(key)

        if value == env_value:
            pass
        else:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0,
                                 winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, env_name, 0, winreg.REG_EXPAND_SZ, env_value)
            winreg.CloseKey(key)

    except WindowsError as e:
        print(e)
        print("Error occurred while trying to add path to system environment variables.")

# if __name__ == '__main__':
# add_system_env("JAVA_HOME", r"D:\\JAVA_12_HOME")
# add_system_env_path(r"%JAVA_HOME%\bin")
