from django.urls import path
from rest_framework.routers import SimpleRouter

from log.views import LogViewSet
from public.views import LoginView, UserViewSet

router = SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"log", LogViewSet, basename="log")
urlpatterns = [
    path(r"login/", LoginView.as_view()),
]