from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    })


def profile(request):
    # You can add more logic here to fetch user-specific data
    return render(request, 'profile.html', {'user': request.user})
