from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class JWTAuthenticationBackend(BaseBackend):
    UserModel = get_user_model()

    def authenticate(self, request, **kwargs):
        try:
            username = request.data.get('username')
            if not username:
                raise Exception("请传入用户名")
            password = request.data.get('password')
            if not password:
                raise Exception("请传入密码")
            user = self.UserModel.objects.get(username=username, password=password)
            return user
        except Exception:
            return None

    def get_user(self, code):
        return self.UserModel.objects.get(pk=code)
