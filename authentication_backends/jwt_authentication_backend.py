from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class JWTAuthenticationBackend(BaseBackend):
    UserModel = get_user_model()

    def authenticate(self, request, **kwargs):
        try:
            username = request.data.get('username')
            if not username:
                raise Exception("Please enter username")
            password = request.data.get('password')
            if not password:
                raise Exception("Please enter password")
            role = request.data.get('role')
            if not role:
                raise Exception("Please enter role")
            user = self.UserModel.objects.get(username=username, password=password, role=role)
            return user
        except Exception:
            return None

    def get_user(self, code):
        return self.UserModel.objects.get(pk=code)
