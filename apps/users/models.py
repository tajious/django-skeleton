from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.core.models import TimestampedModel


class UserManager(BaseUserManager):

    @staticmethod
    def __validate_username(username):
        if username is None:
            raise TypeError('Users must have a username.')

    @staticmethod
    def __validate_email(email):
        if email is None:
            raise TypeError('Users must have an email address.')

    @staticmethod
    def __validate_password(password):
        if password is None:
            raise TypeError('Users must have a password.')

    def create_user(self, username, email, password=None, **kwargs):

        self.__validate_username(username)
        self.__validate_email(email)
        self.__validate_password(password)

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, default='')
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self.__generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __generate_jwt_token(self):
        expiration_date = datetime.now() + timedelta(days=10)
        token_body = {
            'id': self.pk,
            'exp': int(expiration_date.strftime('%s'))
        }
        token = jwt.encode(token_body, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

