from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpRequest, HttpResponse

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user(request=request, user=user)
            return redirect('index')
        print(form.errors)
    else:
        form = StudentRegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_user(request=request, user=user)
                # Redirect to a success page or another URL after successful login
                return redirect('index')  # Replace 'home' with your URL name or path
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
