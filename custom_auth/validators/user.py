from django.db.models import (
    Q
)
from django.core.exceptions import ValidationError

from core.interfaces.validator import ValidatorInterface
from ..models import CustomUser

class UniqueUserWithDocumentNumberValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        document_number = data['document_number']
        queryset  = (
            CustomUser
            .objects
            .filter(
                Q(student__document_number = document_number)|
                Q(teacher__document_number = document_number)
            )
        )

        if queryset.exists():
            raise ValidationError('No puedes continuar con el registro')