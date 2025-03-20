from django.db import models

from core.models import (
    TimeStampedBaseModel
)

class Program(TimeStampedBaseModel):
    """ 
    Modelo de programa, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        name (CharField): Nombre del programa
        code (PositiveIntegerField): Código del programa
    """

    name = models.CharField(
        unique = True,
        max_length = 250,
        verbose_name = 'Nombre'
    )
    code = models.PositiveIntegerField(
        unique = True,
        verbose_name = 'Código'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Programas'

    def __str__(self):
        return self.name