from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user: authenticate = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/accounts/login')
    else:
        if not request.user.is_authenticated:
            return render(request, 'login/login.html')
        else:
            return redirect('/')


def user_logout(request):
    logout(request)
    return redirect('/accounts/login')
