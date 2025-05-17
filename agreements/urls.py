from django.urls import path

from .views import (
    UpdateAgreementDocumentStatusView,
    ToggleStatusAgreementView,
    ToggleStatusDocumentAgreementView
)

urlpatterns = [
    path(
        'agreements/<int:agreement_id>/documents/<int:document_agreement_id>/update-status',
        UpdateAgreementDocumentStatusView.as_view()
    ),
    path('agreements/<int:agreement_id>/toggle-status', ToggleStatusAgreementView.as_view()),
    path('documents/<int:document_id>/toggle-status', ToggleStatusDocumentAgreementView.as_view()),
]