from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

UserModel = get_user_model()

class CurrentRoleBackend(BaseBackend):
    """
    Custom backend that checks user permissions based only on their current role.
    """

    def _get_group_permissions(self, user_obj):
        return user_obj.role.permissions.all()
    
    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = "_%s_perm_cache" % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, "_get_%s_permissions" % from_name)(user_obj)
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(
                user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms}
            )
        return getattr(user_obj, perm_cache_name)
    
    def get_group_permissions(self, user_obj, obj = None):
        return self._get_permissions(user_obj, obj , 'group')
    
    def get_all_permissions(self, user_obj, obj= None):
        return {
            *self.get_user_permissions(user_obj, obj = obj),
            *self.get_group_permissions(user_obj, obj = obj),
        }

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.role:
            raise PermissionDenied()
        if perm in self.get_all_permissions(user_obj, obj = obj):
            return True
        raise PermissionDenied()
