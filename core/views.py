from django.shortcuts import render, redirect
from .camera import VideoCamera
from django.http import StreamingHttpResponse


def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else:
        return render(request, 'home/home.html')


def gen(camera):
    while True:
        try:
            frame = camera.get_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        except:
            break


def video_stream(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else:
        return StreamingHttpResponse(
            gen(VideoCamera()),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
