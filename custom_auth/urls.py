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
    RegisterView
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/validate-password', PasswordValidationView.as_view()),
    path('users/validate-document-number', ValidateInfoUserView.as_view()),
    path('users/register', RegisterView.as_view()),
    
    re_path(r'^users/reset_password/?$', UserViewSet.as_view({'post': 'reset_password'}), name='password-reset'),
    re_path(r'^users/reset_password_confirm/?$', UserViewSet.as_view({'post': 'reset_password_confirm'}), name='password-reset-confirm'),
    re_path(r'^users/set_password/?$', UserViewSet.as_view({'post': 'set_password'}), name='set-password'),
]