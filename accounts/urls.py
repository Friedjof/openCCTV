from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='accounts'),
    path('logout/', views.user_logout, name='logout'),
]
