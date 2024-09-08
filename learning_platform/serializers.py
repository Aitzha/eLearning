from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        # ensures that password is hashed before being saved
        user = User.objects.create_user(**validated_data)
        default_role = Role.objects.get_or_create(name='Student')[0]
        UserProfile.objects.create(user=user, role=default_role)
        return user


class UserProfilePublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    role = serializers.CharField(source='role.name')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role']


class UserProfilePrivateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='role.name')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'role']


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'title', 'content_type']


class SectionSerializer(serializers.ModelSerializer):
    content_items = ContentItemSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'content_items']


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserProfilePrivateSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher']