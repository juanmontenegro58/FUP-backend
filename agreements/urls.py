from django.urls import path

from .views import (
    UpdateAgreementDocumentStatusView
)

urlpatterns = [
    path(
        '<int:agreement_id>/documents/<int:document_agreement_id>/update-status',
        UpdateAgreementDocumentStatusView.as_view()
    )
]