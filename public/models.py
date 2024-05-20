import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    class ROLE(models.TextChoices):
        user = ("U", "User")  # (value, label)
        admin = ("A", "Admin")

    class GENDER(models.IntegerChoices):
        male = (1, "Male")
        female = (0, "Female")

    name = models.CharField(max_length=10)
    gender = models.SmallIntegerField(choices=GENDER.choices, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.user)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    last_login = None
    USERNAME_FIELD = "username"
    objects = BaseUserManager()

    class Meta:
        db_table = 'user'
