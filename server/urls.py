from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.log.views import LogViewSet
from apps.public.views import LoginView, UserViewSet

router = SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"log", LogViewSet, basename="log")
urlpatterns = [
                  path(r"login/", LoginView.as_view()),
                  path('captcha/', include('captcha.urls')),
                  path('captcha/', CaptchaView.as_view()),
              ] + router.urls