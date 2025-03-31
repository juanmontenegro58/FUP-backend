from datetime import datetime

from django.core.exceptions import (
    ValidationError
)

from core.interfaces.validator import (
    ValidatorInterface
)
from ..enums import (
    DefenseStatusEnum
)

class DefenseStatusValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Verifica si la sustentación ya ha sido completada.

        Si el estado de la sustentación es `COMPLETADA`, se lanza una excepción para impedir su reprogramación.

        Args:
            data (dict): Diccionario que contiene la clave `defense`, representando la sustentación (instancia de `Defense`).

        Raises:
            ValidationError: Si la sustentación ya está completada.
        """
        if data['defense'].status == DefenseStatusEnum.COMPLETADA.value:
            raise ValidationError('No se puede reprogramar una sustentación completada.')

class DefenseNewDateValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Valida que la nueva fecha de reprogramación sea distinta a la actual.

        Args:
            data (dict): Diccionario con los datos de la sustentación, debe incluir:
                - `defense` (Defense): Instancia de la sustentación.
                - `new_scheduled_date` (date): Nueva fecha de reprogramación.

        Raises:
            ValidationError: Si la nueva fecha es igual a la actual.
        """
        current_date = data['defense'].scheduled_date
        new_date = data['new_scheduled_date']

        try:
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("El formato de la fecha no es válido. Debe ser 'YYYY-MM-DD'.")
        
        if current_date == new_date:
            raise ValidationError('La nueva fecha de reprogramación debe ser diferente a la actual.')
