import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
from public.utils.file import generate_filtered_file_list


class User(AbstractBaseUser):
    ROLES = (
        ("User", "User"),
        ("Admin", "Admin"),
    )
    GENDERS = (
        (1, "Male"),
        (0, "Female"),
    )
    name = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=GENDERS, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, blank=True, null=True, default="User")
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    last_login = None
    USERNAME_FIELD = "username"
    objects = BaseUserManager()

    class Meta:
        db_table = 'user'

    # def get_file_tree(self):
    #     media_root = os.path.join(settings.MEDIA_ROOT, self.name)
    #     file_tree = {}
    #     if os.path.exists(media_root):
    #         generate_file_tree(media_root, file_tree)
    #     return file_tree

    def get_file_list(self, _filter):
        media_root = os.path.join(settings.MEDIA_ROOT, self.name)
        file_list = []
        time_list = []
        if os.path.exists(media_root):
            generate_filtered_file_list(media_root, file_list, time_list, _filter)
        return file_list
