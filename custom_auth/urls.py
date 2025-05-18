from django.urls import (
    path,
    re_path
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from djoser.views import UserViewSet

from .views import (
    CustomTokenObtainPairView,
    PasswordValidationView,
    ValidateInfoUserView,
    RegisterView,
    PermissionsView,
    PermissionListView
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/users/validate-password', PasswordValidationView.as_view()),
    path('auth/users/validate-document-number', ValidateInfoUserView.as_view()),
    path('auth/users/register', RegisterView.as_view()),
    path('auth/users/permissions', PermissionsView.as_view()),
    
    re_path(r'^auth/users/reset_password_confirm/?$', UserViewSet.as_view({'post': 'reset_password_confirm'}), name='password-reset-confirm'),
    re_path(r'^auth/users/reset_password/?$', UserViewSet.as_view({'post': 'reset_password'}), name='password-reset'),
    re_path(r'^auth/users/set_password/?$', UserViewSet.as_view({'post': 'set_password'}), name='set-password'),
    path('users/me', UserViewSet.as_view({'get': 'me'}), name='me'),
    path('permissions', PermissionListView.as_view()),
]