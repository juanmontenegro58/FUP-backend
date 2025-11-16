"""
URL configuration for fup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (
    path,
    include
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView
)

from agreements.views import (
    AgreementViewSet,
    DocumentAgreementViewSet,
    FavoritosViewSet
)
from companies.views import (
    CompanyViewSet,
    ContactViewSet
)
from programs.views import (
    ProgramViewSet,
    StudentViewSet
)
from evaluations.views import (
    TeacherViewSet,
    DefenseViewSet
)
from practices.views import (
    PracticeViewSet,
    PracticalOfferViewSet
)
from custom_auth.views import (
    UserViewSet,
    RoleViewSet,
)

router = SimpleRouter(trailing_slash = False)
router.register(r'companies', CompanyViewSet, basename = 'company')
router.register(r'contacts', ContactViewSet, basename = 'contact')
router.register(r'documents', DocumentAgreementViewSet, basename = 'document_agreement')
router.register(r'agreements', AgreementViewSet, basename = 'agreement')
router.register(r'programs', ProgramViewSet, basename = 'program')
router.register(r'students', StudentViewSet, basename = 'student')
router.register(r'teachers', TeacherViewSet, basename = 'teacher')
router.register(r'defenses', DefenseViewSet, basename = 'defense')
router.register(r'practices', PracticeViewSet, basename = 'practice')
router.register(r'practical-offers', PracticalOfferViewSet, basename = 'practical-offer')
router.register(r'users', UserViewSet, basename = 'user')
router.register(r'roles', RoleViewSet, basename = 'role')
router.register(r'favoritos', FavoritosViewSet, basename = 'favorito')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('custom_auth.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('agreements.urls')),
    path('api/v1/reports/', include('reports.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]

if settings.DEBUG:
    urlpatterns += [
        path("auth/", include("rest_framework.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
