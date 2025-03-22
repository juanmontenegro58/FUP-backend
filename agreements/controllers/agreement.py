from typing import (
    Dict,
    Any
)

from django.utils import timezone

from core.interfaces.controller import (
    ControllerInterface,
    ControllerMultiRepositoryInterface
)
from core.interfaces.repository import (
    RepositoryInterface
)
from ..models import (
    Agreement,
    AgreementDocumentThrough
)
from ..validators.agreement import (
    AgreementDocumentationStatusValidator,
    AgreementDocumentRelationValidator,
    AgreementDocumentStatusValidator,
    AgreementActiveValidator,
    UniqueStudentInAgreementValidator,
    AgreementDocumentOneRelationValidator,
    AgreementDifferentStatusValidator
)
from programs.models import (
    Student
)
from ..enums import (
    AgreementDocumentStatusEnum
)

class AgreementUploadDocumentController(ControllerInterface):

    """
    Controlador para la carga de documentos asociados a un convenio.

    Este controlador maneja la validación y actualización de documentos en la base de datos.
    """
    
    validations = [
        AgreementDocumentationStatusValidator,
        AgreementDocumentRelationValidator,
        AgreementDocumentStatusValidator
    ]

    def __init__(
        self, 
        raw_data, 
        repository,
        validator,
        agreement_document_through: RepositoryInterface
    ):
        super().__init__(raw_data, repository, validator)
        self.agreement_document_through = agreement_document_through

    def get_agreement(self) -> Agreement:
        """
        Obtiene el convenio asociado al ID proporcionado en los datos de entrada.

        Returns:
            Agreement: Instancia del convenio.
        """
        return (
            self
            .repository
            .get_by_id(
                obj_id = self.raw_data['agreement_id']
            )
        )

    def save_document(
        self, 
        agreement_document_through_id: int,
        data: Dict[str, Any]
    ):
        """
        Actualiza la información de un documento en la base de datos utilizando 
        el modelo intermedio de la relación convenio-documento.

        Args:
            agreement_document_through_id (int): ID de la relación intermedia en la base de datos.
            data (Dict[str, Any]): Datos a actualizar en la relación, como el archivo y metadatos.
        """
        return (
            self
            .agreement_document_through
            .update(
                obj_id = agreement_document_through_id,
                data = data
            )
        )
    
    def build_data(
        self,
        file,
    ) -> Dict[str, Any]:
        """
        Construye los datos que serán almacenados en la relación con el convenio.

        Args:
            file: Archivo a ser cargado.

        Returns:
            Dict[str, Any]: Datos estructurados del documento.
        """
        return {
            'file': file,
            'status': 'SUBIDO',
            'upload_date': timezone.now(),
            'uploaded_by': self.raw_data['user']
        }
    def iter_documents(self) -> None:
        """
        Itera sobre los documentos proporcionados y los guarda en la base de datos.
        """
        files = self.raw_data['files']
        # Se usa through_db ya precargados anteriormente.
        through_ids = self.raw_data['through_db']
        for file, through_id in zip(files, through_ids):
            data = self.build_data(file = file)
            self.save_document(
                agreement_document_through_id = through_id,
                data = data
            )
    
    def preload_data(self):
        """
        Precarga datos necesarios antes de ejecutar la validación.

        Se obtiene el convenio y se filtran las relaciones documento-convenio.
        """

        # Se obtiene la instancia del convenio
        self.raw_data['agreement'] = self.get_agreement()
        # Se obtienen todos los documentos asociados al convenio
        self.raw_data['through_db'] = (
            self
            .agreement_document_through
            .filter(
                pk__in = self.raw_data['through_ids'],
                agreement = self.raw_data['agreement']
            )
        )

    def execute(self):
        """
        Ejecuta el proceso de carga de documentos.

        - Precarga los datos del convenio.
        - Aplica las validaciones definidas.
        - Guarda los documentos en la base de datos.
        """
        self.preload_data()
        self.validator.add_rules(rules = self.validations)
        self.validator.validate(data = self.raw_data)
        self.iter_documents()

class AgreementAssignStudentController(ControllerInterface):

    """
    Controlador para la asignación de un estudiante a un convenio.

    Este controlador gestiona la validación y asignación de un estudiante 
    a un convenio, asegurando que el convenio esté activo y que el estudiante 
    no esté previamente asignado a otro convenio.

    Attrs:
        validations (list): Lista de validadores que se aplicarán antes de 
                            asignar al estudiante.
    """
    
    validations = [
        AgreementActiveValidator,
        UniqueStudentInAgreementValidator
    ]

    def get_student(self) -> Student:
        """
        Obtiene el estudiante a partir del ID proporcionado en los datos de entrada.

        Returns:
            Student: Instancia del estudiante recuperado desde el repositorio.
        """
        return (
            self
            .repository
            .get_by_id(
                obj_id = self.raw_data['student']
            )
        )
    
    def assign_student(self):
        """
        Asigna el estudiante al convenio correspondiente.

        Este método agrega el estudiante a la lista de estudiantes asociados 
        al convenio almacenado en los datos de entrada.
        """
        agreement: Agreement = self.raw_data['agreement']
        agreement.students.add(self.raw_data['student'])
    
    def preload_data(self):
        """
        Precarga los datos necesarios antes de ejecutar la validación.

        Este método obtiene la instancia del estudiante y la almacena en 
        `self.raw_data` para su posterior uso en las validaciones y asignación.
        """

        self.raw_data['student'] = self.get_student()

    def execute(self):
        """
        Ejecuta el proceso de validación y asignación del estudiante al convenio.

        - Precarga los datos necesarios.
        - Agrega las reglas de validación definidas en `validations`.
        - Valida los datos de entrada utilizando los validadores.
        - Asigna el estudiante al convenio si las validaciones son exitosas.

        Raises:
            ValidationError: Si alguna de las validaciones falla.
        """
        self.preload_data()
        self.validator.add_rules(rules = self.validations)
        self.validator.validate(data = self.raw_data)
        self.assign_student()

class UpdateAgreementDocumentStatusController(ControllerMultiRepositoryInterface):

    validations = [
        AgreementDocumentOneRelationValidator,
        AgreementDifferentStatusValidator
    ]

    def get_agreement(self) -> Agreement:
        """
        Obtiene el convenio asociado al ID proporcionado en los datos de entrada.

        Returns:
            Agreement: Instancia del convenio.
        
        Raises:
            ObjectDoesNotExist: Si el documento no existe en el repositorio.
        """
        return (
            self
            .repositories['agreement']
            .get_by_id(
                obj_id = self.raw_data['agreement_id']
            )
        )
    
    def get_document_agreement_through(self) -> AgreementDocumentThrough:
        """
        Obtiene la instancia de AgreementDocumentThrough basada en el ID del documento.

        Returns:
            AgreementDocumentThrough: Instancia del documento del convenio.

        Raises:
            ObjectDoesNotExist: Si el documento no existe en el repositorio.
        """
        return (
            self
            .repositories['agreement_document']
            .get_by_id(
                obj_id = self.raw_data['document_agreement_id']
            )
        )
    
    def preload_data(self):
        """
        Precarga los datos necesarios para la ejecución.

        Obtiene y almacena en `self.raw_data` la información del convenio y 
        del documento del convenio (modelo intermedio AgreementDocumentThrough).
        """
        self.raw_data['agreement'] = self.get_agreement()
        self.raw_data['agreement_document'] = self.get_document_agreement_through()

    def update_status_document(self):
        """
        Actualiza el estado del documento del convenio y guarda los cambios.
        """

        agrement_document: AgreementDocumentThrough = self.raw_data['agreement_document']
        agrement_document.status = self.raw_data['status']
        agrement_document.save()

    def create_comment(self):
        """
        Crea un comentario asociado al cambio de estado del documento.

        Registra el estado anterior, el nuevo estado, el comentario del usuario 
        y la referencia al documento del convenio (modelo intermedio AgreementDocumentThrough).
        """
        data = {
            'previous_state': self.raw_data['agreement_document'].status,
            'new_state': self.raw_data['status'],
            'comment': self.raw_data['comment'],
            'created_by': self.raw_data['user'],
            'agreement_document': self.raw_data['agreement_document']
        }
        self.repositories['comment'].create(**data)
    
    def execute(self):
        """
        Ejecuta el proceso de actualización del estado de un documento de convenio.

        - Precarga los datos requeridos.
        - Valida la información utilizando las reglas definidas.
        - Si el nuevo estado es 'RECHAZADO', crea un comentario asociado.
        - Actualiza el estado del documento del convenio.
        """
        self.preload_data()
        
        self.validator.add_rules(rules = self.validations)
        self.validator.validate(data = self.raw_data)

        if self.raw_data['status'] == AgreementDocumentStatusEnum.RECHAZADO.value:
            self.create_comment()

        self.update_status_document()