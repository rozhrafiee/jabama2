
from rest_framework.permissions import BasePermission

class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'renter')

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'owner')

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
