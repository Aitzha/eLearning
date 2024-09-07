from django.contrib.auth.models import User, Permission
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.user.username

    class Meta:
        # Custom permissions
        permissions = [
            ("change_own_userprofile", "Can change own user profile"),
            ("delete_own_userprofile", "Can delete own user profile")
        ]


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courses_taught')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ContentItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='content_items')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50)  # e.g., 'video', 'pdf'
    file = models.FileField(upload_to='content_files/', blank=True, null=True)  # For PDFs or other documents
    video_url = models.URLField(blank=True, null=True)  # For YouTube videos link
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student.username} on {self.course.title}"
