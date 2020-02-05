#!/usr/bin/env python3
# coding: utf-8
"""
共有的方法
"""

# import sys
# import io
#
# def setup_io():  # 设置默认屏幕输出为utf-8编码
#     sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
#     sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)
# setup_io()

import socket

def check_tcp(ip, port, timeout=1):
    """
    检测tcp端口
    :param ip: ip地址
    :param port: 端口号
    :param timeout: 超时时间
    :return: bool
    """
    flag = False
    try:
        socket.setdefaulttimeout(timeout)  # 整个socket层设置超时时间
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(ip), int(port))
        status = cs.connect_ex((address))  # 开始连接
        cs.settimeout(timeout)

        if not status:
            flag = True

        return flag
    except Exception as e:
        print(e)
        return flag

