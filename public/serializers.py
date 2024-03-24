from rest_framework.serializers import ModelSerializer

from public.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["code", "name"]