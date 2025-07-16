from rest_framework import permissions

class CheckRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'guest':
            return True
        return False

class CheckOffer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'host':
            return True
        return False

class CheckOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


