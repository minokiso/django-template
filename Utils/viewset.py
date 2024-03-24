import traceback
from datetime import datetime
from functools import wraps

from rest_framework import mixins, serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from Utils.response import SuccessResponse, FailureResponse


def handle_error(name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                result = func(self, request, *args, **kwargs)
                return SuccessResponse(result.data if isinstance(result, Response) else result)
            except Exception as e:
                traceback.print_exc()
                return FailureResponse(err=str(e))

        return wrapper

    return decorator


class CreateModelMixinPlus(mixins.CreateModelMixin):
    @handle_error()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RetrieveModelMixinPlus(mixins.RetrieveModelMixin):
    @handle_error()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UpdateModelMixinPlus(mixins.UpdateModelMixin):
    @handle_error()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class DestroyModelMixinPlus(mixins.DestroyModelMixin):
    @handle_error()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = datetime.now().timestamp()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListModelMixinPlus(mixins.ListModelMixin):
    @handle_error()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GenericViewSetPlus(GenericViewSet):
    model = None
    fields = "__all__"
    queryset = None
    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("please provide a model")
        if not self.queryset:
            self.queryset = self.model.objects.all()
        if not self.serializer_class:
            class _ModelSerializer(ModelSerializer):
                class Meta:
                    model = self.model
                    fields = self.fields or "__all__"

            self.serializer_class = _ModelSerializer


class ModelViewSetPlus(CreateModelMixinPlus,
                       RetrieveModelMixinPlus,
                       UpdateModelMixinPlus,
                       DestroyModelMixinPlus,
                       ListModelMixinPlus,
                       GenericViewSetPlus):
    pass
