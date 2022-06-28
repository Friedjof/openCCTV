from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django_otp import devices_for_user, verify_token, match_token


# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        otp = request.POST.get('otp')
        user: authenticate = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if len(tuple(devices_for_user(user))) > 0:
                if match_token(user, otp):
                    login(request, user)
                    return redirect('/')
        # error message because of wrong otp or wrong username/password
        messages.error(request, 'Invalid username, password or OTP')

    if not request.user.is_authenticated:
        return render(request, 'login/login.html')
    else:
        return redirect('/')


def user_logout(request):
    logout(request)
    return redirect('/accounts/login')
