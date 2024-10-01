from django.core.validators import validate_ipv46_address
from django.db import models

# Create your models here.


class Log(models.Model):
    view_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='行为名称')
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name='url')
    time = models.DateTimeField(auto_now_add=True, verbose_name="日志创建时间")
    user_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="用户名")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="账号")
    ip = models.CharField(max_length=60, null=True, blank=True, verbose_name="ip地址",
                          validators=[validate_ipv46_address])

    # comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'log'
        ordering = ["-time"]
