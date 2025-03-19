from django.db import models

from core.models import (
    TimeStampedBaseModel
)

class DocumentAgreement(TimeStampedBaseModel):
    """ 
    Modelo para representar los documentos requeridos para el convenio, 
    hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        name (CharField): Nombre del documento.
        descripcition (Optional[TextField]): Descripción del documento.
        required (BooleanField): El documento es requerido o no.
    """

    name = models.CharField(
        max_length = 100,
        verbose_name = 'Nombre del documento'
    )
    description = models.TextField(
        max_length = 500,
        verbose_name = 'Descripción'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Documentos convenio'

    def __str__(self):
        return self.name