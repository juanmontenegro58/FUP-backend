from django.db import models
 
from core.models import (
    TimeStampedBaseModel
)
from custom_auth.models import (
    CustomUser
)
from .program import (
    Program
)

class Student(TimeStampedBaseModel):
    """ 
    Modelo de estudiante, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        first_name (CharField): Primer nombre
        second_name (Optional[CharField]): Segundo nombre
        first_surname (CharField): Primer apellido
        second_surname (Optional[CharField]): Segundo apellido
        code (PositiveIntegerField): Código de estudiante.
        document_number (CharField): Número de documento.
        email (EmailField): Correo electrónico.
        user (ForeignKey): Relación con el modelo `CustomUser`
        program (ForeignKey): Relación con el modelo `Program`
    """

    first_name = models.CharField(
        max_length = 100,
        verbose_name = 'Primer nombre'
    )
    second_name = models.CharField(
        max_length = 100,
        verbose_name = 'Segundo nombre',
        null = True,
        blank = True 
    )
    first_surname = models.CharField(
        max_length = 100,
        verbose_name = 'Primer apeliido'
    )
    second_surname = models.CharField(
        max_length = 100,
        verbose_name = 'Segundo apellido',
        null = True,
        blank = True
    )
    code = models.PositiveIntegerField(
        verbose_name = 'Código',
        unique = True,
        db_index = True
    )
    document_number = models.CharField(
        max_length = 11,
        verbose_name = 'Número de documento',
        unique = True,
        db_index = True
    )
    email = models.EmailField(
        verbose_name = 'Correo electrónico',
        unique = True
    )
    program = models.ForeignKey(
        Program,
        on_delete = models.CASCADE,
        verbose_name = 'Programa'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.SET_NULL,
        verbose_name = 'Usuario',
        null = True,
        blank = True
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Estudiantes'

    def __str__(self):
        return f'{self.first_name} {self.first_surname}'