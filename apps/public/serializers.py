from captcha.models import CaptchaStore
from django.utils import timezone
from rest_framework.fields import SerializerMethodField, IntegerField, CharField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.public.models import User


class UserSerializer(ModelSerializer):
    children = SerializerMethodField()

    parent_id = PrimaryKeyRelatedField(source='parent', required=True, allow_null=False, queryset=User.objects.all(),
                                       write_only=True)
    key = IntegerField(source='id', read_only=True)
    title = CharField(source='name', read_only=True)

    def get_children(self, obj):
        if obj.children.exists():
            return UserSerializer(obj.children.all(), many=True).data
        return None

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password()
        user.save()

    class Meta:
        model = User
        fields = "__all__"
        depth = 1


class RoleTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['name'] = user.name
        return token

    def validate(self, attrs):
        captcha = self.initial_data.get('captcha')
        if not captcha:
            raise Exception("Please enter captcha")
        captcha_key = self.initial_data.get('captchaKey')
        if not captcha_key:
            raise Exception("Please enter captcha key")
        try:
            now = timezone.now()
            captcha_obj = CaptchaStore.objects.get(response=captcha, hashkey=captcha_key,
                                                   expiration__gt=now)
            captcha_obj.delete()

        except CaptchaStore.DoesNotExist:
            raise Exception("验证码错误")
        return super().validate(attrs)
