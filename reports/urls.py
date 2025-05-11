from django.urls import path

from .views import (
    StatsAgreementView,
    AgreementStatusView,
    ExpirationAgreementView,
    AgreementByYearView,
    AgreementPerProgramView,
    AgreementStudentsView,
    DefenseDashboardView
)

urlpatterns = [
    path('agreements/stats', StatsAgreementView.as_view()),
    path('agreements/status', AgreementStatusView.as_view()),
    path('agreements/expiration', ExpirationAgreementView.as_view()),
    path('agreements/by-year', AgreementByYearView.as_view()),
    path('agreements/per-program', AgreementPerProgramView.as_view()),
    path('agreements/students', AgreementStudentsView.as_view()),

    path('defenses/complete', DefenseDashboardView.as_view()),
]