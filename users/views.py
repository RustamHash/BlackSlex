from django.contrib.auth import logout
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    return redirect('user:login')
