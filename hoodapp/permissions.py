from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsActivatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_active


class Superuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class Admin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff