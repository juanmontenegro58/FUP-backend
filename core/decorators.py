from functools import wraps

from django.core import exceptions

# def user_passes_test(test_func, exc=exceptions.PermissionDenied):
#     def decorator(method):
#         @wraps(method)
#         def _wrapped_method(self, request, *args, **kwargs):
#             if test_func(request.user):
#                 return method(self, request, *args, **kwargs)
#             raise exc()
#         return _wrapped_method
#     return decorator

def user_passes_test(test_func, exc=exceptions.PermissionDenied):
    def decorator(method):
        @wraps(method)
        def _wrapped(*args, **kwargs):
            if hasattr(args[0], "request"):
                request = args[0].request
            else:
                request = args[0]
            if test_func(request.user):
                return method(*args, **kwargs)
            raise exc()
        return _wrapped
    return decorator

superuser_required = user_passes_test(lambda u: u.is_superuser)
staff_member_required = user_passes_test(lambda u: u.is_staff)

def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return user.has_perms(perms)

    return user_passes_test(check_perms)