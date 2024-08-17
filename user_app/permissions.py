from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff members to edit it.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated and (view.kwargs['pk'] == request.user.pk or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated and (obj.pk == request.user.pk or request.user.is_staff)
    
class IsCoachOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow coach or staff members to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_authenticated and (request.user.is_coach or request.user.is_staff)