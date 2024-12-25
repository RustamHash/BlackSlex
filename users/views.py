from django.contrib.auth import logout, authenticate, login as dj_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(request.POST)
            # cd = form.cleaned_data
            # print(cd)
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
        if user and user.is_active:
            dj_login(request, user)
            return redirect('base_app:index')
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'registration/login.html',context=context)
    # return redirect('base_app:index')


def logout_user(request):
    logout(request)
    return redirect('user:login')
