from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from log.models import Log
from public.models import User


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"
        depth = 1
