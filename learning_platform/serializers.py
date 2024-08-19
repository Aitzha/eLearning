from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Role, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

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
        fields = ['username', 'role']


class UserProfilePrivateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='role.name')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role']