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


import os
import time
import socket
import signal
import subprocess
import ipaddress
from multiprocessing import cpu_count
import requests
import json

# def write_log(content,colour='white',skip=False):
#     """
#     写入日志文件
#     :param content: 写入内容
#     :param colour: 颜色
#     :param skip: 是否跳过打印时间
#     :return:
#     """
#     # 颜色代码
#     colour_dict = {
#         'red': 31,  # 红色
#         'green': 32,  # 绿色
#         'yellow': 33,  # 黄色
#         'blue': 34,  # 蓝色
#         'purple_red': 35,  # 紫红色
#         'bluish_blue': 36, # 浅蓝色
#         'white': 37,  # 白色
#     }
#     choice = colour_dict.get(colour)  # 选择颜色
#
#
#     path = os.path.join(conf.BASE_DIR,"output.log") # 日志文件
#     with open(path, mode='a+', encoding='utf-8') as f:
#         if skip is False:  # 不跳过打印时间时
#             content = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + content
#
#         info = "\033[1;{};1m{}\033[0m".format(choice, content)
#         print(info)
#         f.write(content+"\n")


# def valid_ip(ip):
#     """
#     验证ip是否有效,比如192.168.1.256是一个不存在的ip
#     :return: bool
#     """
#     try:
#         # 判断 python 版本
#         if sys.version_info[0] == 2:
#             ipaddress.ip_address(ip.strip().decode("utf-8"))
#         elif sys.version_info[0] == 3:
#             # ipaddress.ip_address(bytes(ip.strip().encode("utf-8")))
#             ipaddress.ip_address(ip)
#
#         return True
#     except Exception as e:
#         print(e)
#         return False

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
#
# def get_host_ip():
#     """
#     查询本机ip地址
#     :return: ip
#     """
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#         return ip
def get_config():
    """
    获取配置中心的配置
    :return:
    """
    config_ip = '127.0.0.1'
    config_port = 8002
    # 判断端口
    if not check_tcp(config_ip, config_port):
        return False

    # 访问api接口
    url = 'http://%s:%s/api/info/'%(config_ip,config_port)
    response = requests.post(url, timeout=1)
    code = response.status_code
    if code != 200:
        print("错误, 访问url: %s异常!" % url)
        return False

    # print(response.content)
    res = (response.content).decode('utf-8')
    res_dict = json.loads(res)

    if not isinstance(res_dict, dict):
        print("错误，获取api: {} 数据失败".format(url), "red")
        return False

    # print("res_dict",res_dict)
    return res_dict
