from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from rest_framework import status
from utils.common import check_tcp
import requests
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "index.html")

@csrf_exempt
def server(request):
    # 各个微服务信息
    server_dict = {
        "auth": {
            "ip": "127.0.0.1",
            "port": 8003,
        },
        "config": {
            "ip": "127.0.0.1",
            "port": 8002,
        },
        "gateway": {
            "ip": "127.0.0.1",
            "port": 8000,
        },
        "user": {
            "ip": "127.0.0.1",
            "port": 8004,
        },
    }

    # 返回 http 200
    return JsonResponse({'status': status.HTTP_200_OK, 'data': server_dict}, status=status.HTTP_200_OK)

@csrf_exempt
def check(request):
    """
    检测几个微服务端口是否正常
    :param request:
    :return:
    """
    response = server(request)
    # print(response.content)
    res = (response.content).decode('utf-8')
    server_dict = json.loads(res)

    if not isinstance(server_dict, dict):
        return JsonResponse(
            {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': 'Failed to get microservice information'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # print("server_dict",server_dict)
    # 状态字典
    ret_dict = {}
    # 遍历
    for i in server_dict['data']:
        # 默认状态为0
        if not ret_dict.get(i):
            ret_dict[i] = 0

        # 检测tcp端口是否正常
        #print("server_dict[i]",server_dict['data'][i]['ip'])
        port_ret = check_tcp(server_dict['data'][i]['ip'], server_dict['data'][i]['port'])
        if port_ret:
            # 更新状态
            ret_dict[i] = 1

    #print("ret_dict",ret_dict)

    # 返回 http 200
    return JsonResponse({'status': status.HTTP_200_OK, 'data': ret_dict}, status=status.HTTP_200_OK)