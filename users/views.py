from django.contrib.auth import logout
from django.shortcuts import render, redirect



def logout_user(request):
    logout(request)
    return redirect('user:login')
