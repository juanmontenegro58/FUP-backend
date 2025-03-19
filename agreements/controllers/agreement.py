from typing import (
    Dict,
    Any
)

from django.utils import timezone

from core.interfaces.controller import (
    ControllerInterface
)
from core.interfaces.repository import (
    RepositoryInterface
)
from ..models import (
    Agreement,
)
from ..validators.agreement import (
    AgreementDocumentationStatusValidator,
    AgreementDocumentRelationValidator,
    AgreementDocumentStatusValidator
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