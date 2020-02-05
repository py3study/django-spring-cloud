from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    # path('info/', views.user_info),
    path('info/', views.GatewayView.as_view({'post':'user_info'}),name='user_info'),
]