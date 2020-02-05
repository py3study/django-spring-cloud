from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    path('info/', views.ConfigView.as_view({'post':'info'}),name='info'),
    path('check/',views.ConfigView.as_view({'get':'check'}),name='check')
]