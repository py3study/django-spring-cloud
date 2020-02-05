from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    # path('login/', views.auth_login),
    path('login/', views.GatewayView.as_view({'post':'auth_login'}),name='login'),
]