import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
from public.utils.file import generate_filtered_file_list


class User(AbstractBaseUser):
    code = models.CharField(max_length=40, db_column='编号', primary_key=True)
    origin = models.CharField(max_length=10, db_column='来源')
    name = models.CharField(max_length=200, db_column='名称')
    username = models.CharField(max_length=10, db_column='账号', unique=True)
    password = models.CharField(max_length=20, db_column='密码', blank=True, null=True)
    last_login = None
    USERNAME_FIELD = "username"
    objects = BaseUserManager()

    class Meta:
        managed = False
        db_table = 'SJDW'

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

    @property
    def is_superuser(self):
        return self.code == settings.SUPER_USER_CODE
