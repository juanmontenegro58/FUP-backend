from django.db import models

from core.models import (
    TimeStampedBaseModel,
    ContactInfoBaseModel
)
from .company import (
    Company
)

class Contact(ContactInfoBaseModel, TimeStampedBaseModel):
    """ 
    Modelo para la representación del contacto, hereda de las clases
    abstractas `ContactInfoBaseModel` y `TimeStampedBaseModel`

    Inherit:
        ContacInfoBaseModel: Proporciona los atributos básicos de contacto
            name (CharField): Nombre.
            phone (CharField): Número de teléfono.
            email (EmailField): Dirección de correo electrónico.
            address (CharField): Dirección física.
        
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        company (ForeignKey): Relación con el modelo `Company`
    
    """

    company = models.ForeignKey(Company, on_delete = models.CASCADE, verbose_name = 'Organización')

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Contactos'

    def __str__(self):
        return self.name