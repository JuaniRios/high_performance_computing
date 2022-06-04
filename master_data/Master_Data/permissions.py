from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


# Custom permission to only allow admin or manager users to use the master data api
class IsAdminOrManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        role = request.user["role"]
        if role == "ADMINISTRATOR" or role == "MANAGER":
            return True

        return False
