from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator

from core import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, phone_number, **extra_fields):
        if not username:
            raise ValueError('username must be set')
        if not password:
            raise ValueError('password must be set')
        if not phone_number:
            raise ValueError('phone_number must be set')

        username = self.model.normalize_username(username)
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(username, password, phone_number, **extra_field)

    def create_staff(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(username, password, phone_number, **extra_field)

    def create_superuser(self, username, password, phone_number, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        return self._create_user(username, password, phone_number, **extra_field)


class User(AbstractBaseUser, models.AbstractBaseModel, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^0\d{9,11}$',
                                 message="number must be entered in the format: '09...' 9 Up to 15 digits allowed.")
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_regex])
    gender = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return f'[{self.id}] {self.first_name} {self.last_name}'
