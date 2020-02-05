from django.conf.urls import url
from django.urls import path
from application import views

urlpatterns = [
    path('api-auth/login/', views.UsersView.as_view({'post':'login'})),
    path('api-docs/', views.UsersView.as_view({'post':'docs'})),
]