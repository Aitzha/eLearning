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
        fields = ['id', 'section', 'title', 'content_type', 'file', 'video_url', 'order']

    def to_representation(self, instance):
        # Custom representation for the content type
        representation = super().to_representation(instance)

        # Only include the relevant field based on content_type
        if instance.content_type == 'pdf':
            representation.pop('video_url', None)
        elif instance.content_type == 'video':
            representation.pop('file', None)

        return representation


class SectionSerializer(serializers.ModelSerializer):
    content_items = ContentItemSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'content_items']


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserProfilePrivateSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), write_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_id']

    def create(self, validated_data):
        # Pop teacher_id from validated_data and use it to set the teacher
        teacher_id = validated_data.pop('teacher_id')
        validated_data['teacher'] = teacher_id
        return super().create(validated_data)