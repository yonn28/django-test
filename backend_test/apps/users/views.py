from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import LoginForm , RegistroForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
# Create your views here.

def login_user(request):
    "Login user"
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],  password=cd['password'])
            if user is not None:
                login( request, user )
                return HttpResponseRedirect(reverse_lazy('notifications:create'))
            else:
                return HttpResponse('Authentication failed!, please try again!')
    else:
        form = LoginForm()
    return render(request,'login/login.html',context={'form':form})

def register(request):
    "register a new user"
    if request.method == 'POST':
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('users:login'))
    else:
        form = UserCreationForm()
    return render(request,'login/registry.html',context={'form': form})

def logout_user(request):
    "logout a user"
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))