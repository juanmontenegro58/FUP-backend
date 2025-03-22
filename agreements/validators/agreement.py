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
from ..repositories.agreement import (
    AgreementStudentThroughRepository
)
from ..models import (
    Agreement,
    AgreementDocumentThrough
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

class AgreementActiveValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Verifica que el convenio tenga el estado `ACTIVO`.

        Este método revisa si el convenio proporcionado en los datos de entrada 
        tiene el estado 'ACTIVO'. Si el convenio no está activo, se lanza una excepción 
        para evitar la continuación del proceso.

        Args:
            data (dict): Un diccionario que contiene la clave `agreement`, 
                        la cual debe ser la instancia del modelo `Agreement`.

        Raises:
            ValidationError: Se lanza si el convenio no se encuentra activo.
        """
        if data['agreement'].status != 'ACTIVO':
            raise ValidationError('El convenio no se encuentra activo.')

class UniqueStudentInAgreementValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """
        Verifica que el estudiante no esté asignado a un convenio existente.

        Este método consulta el repositorio de convenios-estudiantes para determinar 
        si el estudiante ya está vinculado a algún convenio con estado `ACTIVO`. Si se encuentra una coincidencia, 
        se lanza una excepción para evitar la duplicación.

        Args:
            data (dict): Un diccionario que contiene la clave `student`, 
                        que es una instancia del modelo `Student`.

        Raises:
            ValidationError: Se lanza si el estudiante ya está asignado a un convenio.
        """
        repository = AgreementStudentThroughRepository()
        queryset = (
            repository
            .filter(
                student = data['student']
            )
        )
        if queryset.exists():
            raise ValidationError('El estudiante ya se encuentra asignado a un convenio.')
        
class AgreementDocumentOneRelationValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """Verifica si el documento está asociado al acuerdo antes de permitir su modificación.

        Args:
            data (dict): Datos necesarios para la validación.
                - agreement (Agreement): Acuerdo al que debería pertenecer el documento.
                - document_agreement_id (int): ID del documento que se intenta modificar, este id debe ser del modelo intermedio AgreementDocumentThrough.

        Raises:
            PermissionDenied: Si el documento no está relacionado con el acuerdo.
        """
        
        agreement: Agreement = data['agreement']

        if not agreement.agreementdocumentthrough_set.filter(
            document_agreement__id = data['document_agreement_id']
        ).exists():
            raise PermissionDenied('No estas autorizado para la modificación de este documento.')

class AgreementDifferentStatusValidator(ValidatorInterface):

    @staticmethod
    def validate(data):
        """Impide que un documento mantenga el mismo estado cuando se intenta actualizar.

        Args:
            data (dict): Datos necesarios para la validación.
                - document_agreement (AgreementDocumentThrough): Documento del acuerdo a modificar.
                - status (str): Nuevo estado que se desea asignar.

        Raises:
            ValidationError: Si el nuevo estado es igual al estado actual del documento.
        """
        
        document_agreement: AgreementDocumentThrough = data['agreement_document']

        if document_agreement.status == data['status']:
            raise ValidationError('El nuevo estado no puede ser el mismo que el actual.')