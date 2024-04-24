import os
import traceback

from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from Utils.response import SuccessResponse, FailureResponse
from Utils.viewset import ModelViewSetPlus
from log.views import create_log
from public.models import User
from public.serializers import UserSerializer


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
