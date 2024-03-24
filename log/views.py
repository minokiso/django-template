# Create your views here.
import traceback

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet

from Utils.response import SuccessResponse, FailureResponse
from log.models import Log
from log.serializers import LogSerializer


class LogViewSet(GenericViewSet, ListModelMixin):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def list(self, request, *args, **kwargs):
        try:
            is_superuser = request.user.is_superuser
            print(request.query_params.get('page_size'))
            if not is_superuser:
                self.queryset = self.get_queryset().filter(username=request.user.username)
            result = super().list(request, *args, **kwargs)
            return SuccessResponse(data=result.data)
        except Exception as e:
            return FailureResponse(str(e))


def create_log(name, log_model=Log):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            result = func(self, request, *args, **kwargs)
            try:
                if not isinstance(result, FailureResponse):
                    log_model.objects.create(
                        name=name,
                        url=request.path,
                        ip=get_client_ip(request),
                        user_name=request.user.name,
                        username=request.user.username,
                    )
            except Exception as e:
                print("日志创建失败")
                traceback.print_exc()
            return result

        return wrapper

    return decorator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 取 X-Forwarded-For 列表中的第一个 IP 地址
    else:
        ip = request.META.get('REMOTE_ADDR')  # 直接从 REMOTE_ADDR 获取 IP 地址
    return ip
