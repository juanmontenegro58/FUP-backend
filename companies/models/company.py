from django.db import models

from core.models import (
    TimeStampedBaseModel,
    ContactInfoBaseModel
)

class Company(ContactInfoBaseModel, TimeStampedBaseModel):
    """  
    Modelo de compañia, hereda de las clases 
    abstractas ContacInfoBaseModel y TimeStampedBaseModel.

    Inherit:
        ContacInfoBaseModel: Proporciona los atributos básicos de contacto
            name (CharField): Nombre.
            phone (CharField): Número de teléfono.
            email (EmailField): Dirección de correo electrónico.
            address (CharField): Dirección física.
        
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attribute:
        nui (CharField): Número único de identificación de la organización.
    """

    nui = models.CharField(
        max_length = 20,
        verbose_name = 'Número único de identificación',
        unique = True
    )

    class Meta:
        verbose_name_plural: str = 'Organizaciones'

    def __str__(self):
        return self.name