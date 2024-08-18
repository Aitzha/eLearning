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
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = [
            ("change_own_userprofile", "Can change own user profile"),
            ("view_own_userprofile", "Can view own user profile"),
            ("delete_own_userprofile", "Can delete own user profile")
        ]
