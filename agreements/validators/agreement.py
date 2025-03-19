from django.core.exceptions import (
    ValidationError,
    PermissionDenied
)

from core.interfaces.validator import (
    ValidatorInterface
)

from ..enums import (
    AgreementDocumentationStatusEnum,
    AgreementDocumentStatusEnum
)

class AgreementDocumentationStatusValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Verifica si la documentación del convenio ya está marcada como completa.

        Si el estado de la documentación es `COMPLETA`, se lanza una excepción para impedir modificaciones.

        Args:
            data (dict): Diccionario que contiene la clave `agreement`, representando el convenio.

        Raises:
            ValidationError: Si la documentación ya está completa.
        """
        if data['agreement'].documentation_status.upper() == AgreementDocumentationStatusEnum.COMPLETA.value:
            raise ValidationError('No se puede actualizar la documentación.')

class AgreementDocumentRelationValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Verifica que los documentos proporcionados coincidan con los almacenados en la base de datos.

        Se compara la cantidad de documentos obtenidos en `through_db` con la cantidad
        de `through_ids` recibidos para asegurar que el usuario solo modifique los documentos permitidos.

        Args:
            data (dict): Diccionario que incluye `through_db` (documentos en la BD) y `through_ids` (IDs recibidos).

        Raises:
            PermissionDenied: Si la cantidad de documentos en `through_db` no coincide con `through_ids`,
                              lo que indica que el usuario no está autorizado para modificarlos.
        """
        if data['through_db'].count() != len(data['through_ids']):
            raise PermissionDenied('No estas autorizado para subir estos documentos.')

class AgreementDocumentStatusValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Recorre los documentos intermedios (`through_db`) y verifica su estado.

        No permite la actualización de documentos que ya tengan el estado `APROBADO`.

        Args:
            data (dict): Diccionario que contiene la lista `through_db` con los documentos de la tabla intermedia a validar.

        Raises:
            ValidationError: Si al menos un documento ya ha sido aprobado.
        """
        for item in data['through_db']:
            if item.status.upper() == AgreementDocumentStatusEnum.APROBADO.value:
                raise ValidationError('No se puede actualizar un documento cuando esta aprobado.')