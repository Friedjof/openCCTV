from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse


from .camera import VideoCamera
from .streamManager import StreamManager


stream_manager = StreamManager()


def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else:
        return render(request, 'home/home.html')


def video_stream(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else:
        return StreamingHttpResponse(
            VideoCamera(stream_manager).loop(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )


def settings(request):
    return render(request, 'camera/settings/index.html')
