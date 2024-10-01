import traceback
from functools import wraps

from django.http import JsonResponse
from rest_framework.response import Response
from loggers import http_logger

from Utils.response import SuccessResponse, FailureResponse


def handle_error(name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                result = func(self, request, *args, **kwargs)
                return SuccessResponse(result.data if isinstance(result, Response) else result)
            except Exception as e:
                http_logger.error(traceback.format_exc())
                return FailureResponse(err=str(e))

        return wrapper

    return decorator


def handle_async_error(name=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, request, *args, **kwargs):
            try:
                result = await func(self, request, *args, **kwargs)
                return JsonResponse({"data": result, "msg": "success", "code": 0}, json_dumps_params={'ensure_ascii': False})
            except Exception as e:
                traceback.print_exc()
                return JsonResponse({"data": None, "msg": str(e), "code": 400}, json_dumps_params={'ensure_ascii': False})

        return wrapper

    return decorator
