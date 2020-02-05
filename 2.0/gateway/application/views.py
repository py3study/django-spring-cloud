from django.shortcuts import render,redirect,HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from rest_framework import status
import requests
import json
from utils.common import check_tcp

def get_server_info():
    """
    获取配置中心的配置
    :return:
    """
    config_ip = 'svc-config.default.svc.cluster.local'
    config_port = 8001
    # 访问api接口
    url = 'http://%s:%s/server/'%(config_ip,config_port)
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


# Create your views here.
class GatewayView(ViewSetMixin, APIView):  # 用户表
    def eureka(self, request, *args, **kwargs):
        """
        eureka
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        eureka_ip = 'svc-eureka.default.svc.cluster.local'
        eureka_port = 8001
        url = 'http://%s:%s/server/'%(eureka_ip,eureka_port)
        response = requests.post(url, timeout=2)
        res = (response.content).decode('utf-8')
        res_dict = json.loads(res)

        if not isinstance(res_dict, dict):
            # print("错误，获取api: {} 数据失败".format(url), "red")
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Data returned by auth api is abnormal'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res_dict)

    def config(self, request, *args, **kwargs):
        """
        配置中心信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        config_ip = 'svc-config.default.svc.cluster.local'
        config_port = 8002
        url = 'http://%s:%s/api/info/'%(config_ip,config_port)
        response = requests.post(url, timeout=2)
        res = (response.content).decode('utf-8')
        res_dict = json.loads(res)

        if not isinstance(res_dict, dict):
            # print("错误，获取api: {} 数据失败".format(url), "red")
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Data returned by auth api is abnormal'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res_dict)
        # return redirect('http://127.0.0.1:8002/api/info/')

    def auth_login(self, request, *args, **kwargs):
        """
        用户认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # print('http://127.0.0.1:8003/api-auth/login/')
        # return redirect('http://127.0.0.1:8003/api-auth/login/')
        user_post = request.POST.get("username")
        pwd_post = request.POST.get("password")

        data = {
            'username':user_post,
            'password': pwd_post,
        }

        auth_ip = "svc-auth.default.svc.cluster.local"
        auth_port = 8003
        if not check_tcp(auth_ip,auth_port):
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Authentication microservice port unreachable'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = 'http://%s:%s/api-auth/login/'%(auth_ip,auth_port)
        response = requests.post(url,data=data, timeout=2)
        res = (response.content).decode('utf-8')
        res_dict = json.loads(res)

        if not isinstance(res_dict, dict):
            # print("错误，获取api: {} 数据失败".format(url), "red")
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Data returned by auth api is abnormal'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res_dict)

    def user_info(self, request, *args, **kwargs):
        """
        用户认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_post = request.POST.get("username")
        pwd_post = request.POST.get("password")

        data = {
            'username': user_post,
            'password': pwd_post,
        }
        user_ip = 'svc-user.default.svc.cluster.local'
        user_port = 8004
        url = 'http://%s:%s/api-user/info/'%(user_ip,user_port)
        response = requests.post(url, data=data, timeout=2)
        res = (response.content).decode('utf-8')
        res_dict = json.loads(res)

        if not isinstance(res_dict, dict):
            # print("错误，获取api: {} 数据失败".format(url), "red")
            return JsonResponse(
                {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Data returned by auth api is abnormal'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res_dict)
