from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video_stream', views.video_stream, name='video_stream'),
    path('settings', views.settings, name='settings'),
]
