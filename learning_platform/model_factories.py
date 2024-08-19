import factory
from .models import *
from django.contrib.auth.models import User, Permission


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = "Student"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Creates unique username for every user instance created
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    # Ensures that password is hashed before being stored
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)