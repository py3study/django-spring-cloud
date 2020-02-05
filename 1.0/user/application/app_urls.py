from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    path('info/', views.UsersView.as_view({'post':'info'}),name='info'),
    path('check/',views.UsersView.as_view({'get':'check'}),name='check')
]