from django.shortcuts import render, HttpResponse, redirect, reverse
import time, json
from application import models
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from rest_framework import status
from utils.mysql_tools import ExecutionSql
from utils.common import get_config,check_tcp


# Create your views here.
class UsersView(ViewSetMixin, APIView):  # 用户表
    def info(self, request, *args, **kwargs):
        """
        用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 获取配置信息
        res_dict = get_config()
        if not res_dict:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to get configuration'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 获取表单数据
        user_post = request.POST.get("username")
        # pwd_post = request.POST.get("password")
        # print(user_post, pwd_post)

        # 获取mysql连接信息
        host = res_dict['data']['mysql'].get('host')
        user = res_dict['data']['mysql'].get('username')
        password = res_dict['data']['mysql'].get('password')
        port = res_dict['data']['mysql'].get('port')

        # 判断mysql端口
        if not check_tcp(host, port):
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'MySQL port cannot connect'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 查询表记录
        sql = "select * from usercenter.users where username='%s'" % (
            user_post)
        print(sql)
        mysql_obj = ExecutionSql(host, user, password, port)
        user_info = mysql_obj.select(sql)

        # 判断执行结果
        if not user_info:
            # 返回 http 500
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to query user information'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 返回 http 200
        return JsonResponse({'status': status.HTTP_200_OK, 'data': [user_info]}, status=status.HTTP_200_OK)

    def check(self, request, *args, **kwargs):
        """
        服务自检
        :param request:
        :return:
        """
        # 判断 eureka 注册中心是否启动
        port_ret = check_tcp('127.0.0.1', '8001')
        if not port_ret:
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Eureka Micro service Not started'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 判断config 微服务是否启动
        port_ret = check_tcp('127.0.0.1', '8002')
        if not port_ret:
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Config Micro service Not started'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 判断获取配置信息
        res_dict = get_config()
        if not res_dict:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to get configuration'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 判断mysql连接
        # 获取mysql连接信息
        host = res_dict['data']['mysql'].get('host')
        user = res_dict['data']['mysql'].get('username')
        password = res_dict['data']['mysql'].get('password')
        port = res_dict['data']['mysql'].get('port')

        # 判断mysql端口
        if not check_tcp(host, port):
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'MySQL port cannot connect'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 查询表记录
        sql = "show databases"
        print(sql)
        mysql_obj = ExecutionSql(host, user, password, port)

        select_ret = mysql_obj.select(sql)
        if not select_ret:
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to detect MySQL connection'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 返回 http 200
        return JsonResponse({'status': status.HTTP_200_OK, 'data': []}, status=status.HTTP_200_OK)

    def docs(self, request, *args, **kwargs):
        """
        api文档
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = {
            "swagger": "1.0",
            "info": {
                "version": "1.0",
                "title": "接口文档"
            },
            "host": "127.0.0.1",
            "basePath": "/api-user/",
            "tags": [
                {
                    "name": "info接口",
                    "description": "user Controller"
                },
            ]
        }
        return JsonResponse({'status': status.HTTP_200_OK, 'data': data}, status=status.HTTP_200_OK)

def swagger(request):
    """
    swagger接口文档
    :param request:
    :return:
    """
    return render(request, "swagger-ui.html")