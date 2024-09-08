from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request, 'index.html', {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    })


def profile(request):
    return render(request, 'profile.html', {'user': request.user})


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'registration.html')


def course_list(request):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    return render(request, "courses.html", {'page_size': page_size})


def teacher_manager(request):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    return render(request, "teacher-manager.html", {'page_size': page_size})


def course_create(request):
    return render(request, 'course-create.html')


def course_details(request, course_id):
    return render(request, 'course-details.html', {'course_id': course_id})


def course_edit(request, course_id):
    return render(request, 'course-edit.html', {'course_id': course_id})


def section_edit(request, section_id):
    return render(request, 'section-edit.html', {'section_id': section_id})


def add_content(request, section_id):
    return render(request, 'content-form.html', {'section_id': section_id})


def content_edit(request, content_id):
    return render(request, 'content-form.html', {'content_id': content_id})
