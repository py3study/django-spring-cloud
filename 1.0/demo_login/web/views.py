from django.shortcuts import render,HttpResponse

# Create your views here.
def login(request):
    return render(request, "login.html")

def index(request):
    return render(request, "index.html")

def config(request):
    return render(request, "config.html")

def user_info(request):
    # 临时固定数据
    username = "xiao"
    password = "1234"
    data = {
        "username":username,
        "password": password,
    }
    return render(request, "user_info.html",data)
