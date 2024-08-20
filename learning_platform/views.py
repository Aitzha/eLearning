from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html', {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    })


def profile(request):
    # You can add more logic here to fetch user-specific data
    return render(request, 'profile.html', {'user': request.user})


def login(request):
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')