import os
import traceback
import uuid
from pathlib import Path

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf import settings
from django.http import HttpResponse, FileResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from Utils.response import SuccessResponse, FailureResponse
from Utils.viewset import ModelViewSetPlus, handle_error
from apps.log.views import create_log
from apps.public.models import User
from apps.public.serializers import UserSerializer
from loggers import http_logger


class UserViewSet(ModelViewSetPlus):
    model = User
    search_fields = ["name", "username"]
    filterset_fields = {
        "name": ["icontains"],
        "username": ["icontains"],
        "parent": ["exact"],
    }
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(pk=request.user.pk)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        user = super().create(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    permission_classes = []

    @create_log("管理端登录")
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid()
                request.user = serializer.user
                return SuccessResponse(data=serializer.validated_data)
            except TokenError as e:
                raise InvalidToken(e.args[0])

        except AuthenticationFailed as e:
            http_logger.error(traceback.format_exc())
            return FailureResponse(err="用户名或密码不正确")
        except Exception as e:
            http_logger.error(traceback.format_exc())
            return FailureResponse(err=str(e))


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


class MediaView(APIView):
    permission_classes = []

    def get(self, request, path):
        try:
            file_path = Path(settings.MEDIA_ROOT) / path
            if not file_path.is_file() or not file_path.exists():
                raise Exception("文件不存在")
            return FileResponse(file_path.open('rb'))
        except Exception as e:
            http_logger.error(traceback.format_exc())
            return FailureResponse(str(e))


class UploadView(APIView):
    @handle_error()
    def post(self, request, path):
        file = request.FILES.get("file")
        if not file:
            raise FileNotFoundError("未传递文件")
        upload_dir = Path(settings.MEDIA_ROOT) / path
        if not upload_dir.is_dir():
            raise NotADirectoryError("目录不存在")
        file_name = f"{uuid.uuid4()}{os.path.splitext(file.name)[1]}"
        file_path = upload_dir / file_name
        with file_path.open('wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return f"{path}/{file_name}"
