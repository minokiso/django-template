from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    class ROLE(models.TextChoices):
        admin = ("A", "Admin")
        proxy = ("P", "Proxy")
        user = ("U", "User")  # (value, label)

    name = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.user)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    remark = models.TextField(blank=True, null=True)
    enable = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)

    last_login = None
    USERNAME_FIELD = "username"
    objects = BaseUserManager()

    class Meta:
        db_table = 'user'

    def save(self, *args, **kwargs):
        if self.parent.role == self.ROLE.user:
            raise Exception("不能选择用户作为上级")

        parent_self_role_map = {
            self.ROLE.admin: self.ROLE.proxy,
            self.ROLE.proxy: self.ROLE.user
        }

        if self.parent is None:
            self.role = self.ROLE.admin
        else:
            self.role = parent_self_role_map[self.parent.role]
        if self.role == self.ROLE.user and self.children.all().exists():
            raise Exception("不能将有下级的代理降级为普通用户")
        super().save(*args, **kwargs)
        
    def is_enable(self):
        if self.enable and self.parent:
            return self.parent.is_enable()
        return self.enable

