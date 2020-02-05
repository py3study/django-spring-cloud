from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    path('login/', views.UsersView.as_view({'post':'login'}))
]