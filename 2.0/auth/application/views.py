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
    def login(self, request, *args, **kwargs):
        """
        登录
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
        pwd_post = request.POST.get("password")
        print("post",user_post, pwd_post)

        # 获取mysql连接信息
        host = res_dict['data']['mysql'].get('host')
        user = res_dict['data']['mysql'].get('username')
        password = res_dict['data']['mysql'].get('password')
        port = res_dict['data']['mysql'].get('port')

        print("host",host,port)
        # 判断mysql端口
        if not check_tcp(host,port):
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'MySQL port cannot connect'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print("查询表记录。。。。")
        # 查询表记录
        sql = "select username,password from usercenter.users where username='%s' and password=md5('%s')" % (
            user_post, pwd_post)
        print(sql)
        mysql_obj = ExecutionSql(host, user, password, port)
        auth_ret = mysql_obj.select(sql)

        # 判断执行结果
        if not auth_ret:
            # 返回 http 401
            return JsonResponse({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Authentication failure'},
                                status=status.HTTP_401_UNAUTHORIZED)

        # 更新登录时间
        last_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # UPDATE table_name SET field1=new-value1, field2=new-value2
        sql = "update usercenter.users set last_time='%s' where username='%s'" % (last_time, user_post)
        print(sql)
        update_ret = mysql_obj.update(sql)
        if not update_ret:
            return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to update login time'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 登录成功
        # 返回 http 200
        return JsonResponse({'status': status.HTTP_200_OK, 'data': []}, status=status.HTTP_200_OK)

    def check(self, request, *args, **kwargs):
        """
        服务自检
        :param request:
        :return:
        """
        # 判断 eureka 注册中心是否启动
        port_ret = check_tcp('svc-eureka.default.svc.cluster.local', '8001')
        if not port_ret:
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Eureka Micro service Not started'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 判断config 微服务是否启动
        port_ret = check_tcp('svc-config.default.svc.cluster.local', '8002')
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
            "host": "svc-auth.default.svc.cluster.local",
            "basePath": "/api-auth/",
            "tags": [
                {
                    "name": "login接口",
                    "description": "auth Controller"
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