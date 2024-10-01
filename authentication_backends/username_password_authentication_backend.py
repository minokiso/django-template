import traceback

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from loggers import http_logger


class UsernamePasswordAuthenticationBackend(BaseBackend):
    UserModel = get_user_model()

    def authenticate(self, request, **kwargs):
        try:
            username = request.data.get('username')
            if not username:
                raise Exception("请输入用户名")
            password = request.data.get('password')
            if not password:
                raise Exception("请输入密码")
            user = self.UserModel.objects.get(username=username)
            if user.check_password(password):
                raise Exception("用户名或密码错误")
            return user
        except Exception:
            http_logger.error(traceback.format_exc())
            return None

    def get_user(self, user_id):
        return self.UserModel.objects.get(pk=user_id)
