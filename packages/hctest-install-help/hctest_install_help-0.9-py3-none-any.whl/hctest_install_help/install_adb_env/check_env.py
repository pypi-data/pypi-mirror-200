# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：check_env.py
import subprocess


def check_java():
    try:
        # 使用管道捕获命令行输出
        proc = subprocess.Popen(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, out = proc.communicate()
        # 检查输出以确定是否安装了 Java
        if err or b'java version' not in out:
            print('没有装java环境')
        else:
            print('java环境检测通过')
    except OSError:
        print('没有装java环境')


if __name__ == '__main__':
    check_java()
