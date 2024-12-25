from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    return redirect('user:login')
