import traceback

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from Utils.response import SuccessResponse, FailureResponse
from apps.log.models import Log
from apps.log.serializers import LogSerializer
from loggers import http_logger


class LogViewSet(GenericViewSet, ListModelMixin):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


def create_log(view_name, log_model=Log):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            result = func(self, request, *args, **kwargs)
            try:
                if not isinstance(result, FailureResponse):
                    log_model.objects.create(
                        view_name=view_name,
                        url=request.path,
                        ip=get_client_ip(request),
                        user_name=request.user.name,
                        username=request.user.username,
                    )
            except Exception as e:
                http_logger.error(traceback.format_exc())
                http_logger.error("日志创建失败")

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
