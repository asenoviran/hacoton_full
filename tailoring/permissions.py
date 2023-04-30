from rest_framework.permissions import BasePermission



class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_owner
        return False
    
class IsOwnerAndAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_owner and obj.owner == request.user
        return False


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user