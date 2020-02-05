from django.shortcuts import render,HttpResponse, redirect,reverse
import time,json
# from api import models
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from rest_framework import status
from utils.common import check_tcp,get_config
from utils.mysql_tools import ExecutionSql

# Create your views here.
class ConfigView(ViewSetMixin,APIView):  # 用户表
    def info(self, request, *args, **kwargs):
        """
        中间件连接信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        config_dict = {
            "mysql":{
                "host":"192.168.31.229",
                "port": 3306,
                "username": "root",
                "password": "abcd@1234",
            }
        }
        # 返回 http 200
        return JsonResponse({'status': status.HTTP_200_OK, 'data': config_dict}, status=status.HTTP_200_OK)

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

        # 判断获取配置信息
        response = self.info(request)
        res = (response.content).decode('utf-8')
        res_dict = json.loads(res)
        # print("res_dict",res_dict)
        if not res_dict:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to get configuration'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 判断mysql连接
        # 获取mysql连接信息
        host = res_dict['data']['mysql'].get('host')
        user = res_dict['data']['mysql'].get('username')
        password = res_dict['data']['mysql'].get('password')
        port = res_dict['data']['mysql'].get('port')

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