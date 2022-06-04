from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

# Custom permission classes for limiting views to a specific role


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser)


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user["role"] == "ADMINISTRATOR"


class IsSecretary(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user["role"] == "SECRETARY"


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user["role"] == "MANAGER"
