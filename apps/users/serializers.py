import re

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number', 'address', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_phone_number(self, value):
        if not re.match('^(0)?9\d{9}$', value):
            raise serializers.ValidationError(
                'Please use a valid phone number'
            )

        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                'Phone number already exists.'
            )

        return value

    def validate_email(self, value):
        if not re.match('[^@]+@[^@]+\.[^@]+', value):
            raise serializers.ValidationError(
                'Please use a valid email address'
            )

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email already exists.'
            )

        return value

    def validate_username(self, value):
        if not re.match('^[a-zA-Z0-9]+(?:[_-]?[a-zA-Z0-9])*$', value):
            raise serializers.ValidationError(
                'Please use a valid username.'
            )

        if User.objects.filter(username=value):
            raise serializers.ValidationError(
                'Username already exists.'
            )

        return value


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'A username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'phone_number': user.phone_number,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number', 'address',)
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
