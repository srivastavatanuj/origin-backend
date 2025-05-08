from rest_framework import permissions
from .models import User, StaffProfile


class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True

        try:
            all_managers = StaffProfile.objects.filter(
                role='manager').values_list('user', flat=True)
            if user.id in all_managers:
                return True
        except StaffProfile.DoesNotExist:
            pass
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True

        return False


class IsBuyerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user)
        if user.is_staff == False:
            return True

        return False
