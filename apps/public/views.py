import os
import traceback

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from Utils.response import SuccessResponse, FailureResponse
from Utils.viewset import ModelViewSetPlus, handle_error
from apps.log.views import create_log
from apps.public.models import User


class UserViewSet(ModelViewSetPlus):
    model = User
    search_fields = ["name", "username"]
    filterset_fields = {
        'gender': ['exact']
    }


class LoginView(TokenObtainPairView):
    @create_log("登录")
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                request.user = serializer.user
                return SuccessResponse(data=serializer.validated_data)
            except TokenError as e:
                raise InvalidToken(e.args[0])

        except AuthenticationFailed as e:
            traceback.print_exc()
            return FailureResponse(err="用户名或密码不正确")
        except Exception as e:
            traceback.print_exc()
            return FailureResponse(err=str(e))


class FileView(ViewSet):
    def list(self, request):
        try:
            files = request.user.get_file_list(request.query_params.get('filter'))
            return SuccessResponse(files)
        except Exception as e:
            traceback.print_exc()
            return FailureResponse(str(e))

    @create_log("下载文件")
    def retrieve(self, request, path):
        try:
            if '..' in path or path.startswith('/'):
                raise ValueError("文件路径不正确")
            filepath = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(filepath):
                raise FileExistsError("文件不存在")
            with open(filepath, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                return response
        except Exception as e:
            return FailureResponse(str(e))


class CaptchaView(APIView):
    permission_classes = []

    @handle_error()
    def get(self, request):
        # 生成验证码
        key = CaptchaStore.generate_key()
        # 获取验证码图片的URL
        url = captcha_image_url(key)
        if isinstance(url, HttpResponse):
            raise Exception('获取验证码失败')
        return {"key": key, "url": url}
