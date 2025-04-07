from django.db import models

from core.models import (
    TimeStampedBaseModel
)
from .choices import (
    PRACTICE_STATUS_CHOICES
)
from programs.models import (
    Student
)
from evaluations.models import (
    Teacher
)
from .practical_offer import (
    PracticalOffer
)

class Practice(TimeStampedBaseModel):
    """ 
    Modelo de práctica, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        initial_date (DateField): Fecha de inicio.
        end_date (DateField): Fecha de finalización.
        status (CharField): Estado de la práctica.
        student (ForeignKey): Relación con el modelo `Student`
        teacher (ForeignKey): Relación con el modelo `Teacher`
        practical_offer (ForeignKey): Relación con el modelo `PracticalOffer`
    """

    initial_date = models.DateField(
        verbose_name = 'Fecha de inicio'
    )
    end_date = models.DateField(
        verbose_name = 'Fecha de finalización'
    )
    status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado',
        default = 'PENDIENTE',
        choices = PRACTICE_STATUS_CHOICES
    )
    student = models.ForeignKey(
        Student,
        on_delete = models.PROTECT,
        verbose_name = 'Estudiante'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete = models.PROTECT,
        verbose_name = 'Docente'
    )
    practical_offer = models.ForeignKey(
        PracticalOffer,
        on_delete = models.PROTECT,
        verbose_name = 'Oferta práctica',
        null = True,
        blank = True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural: str = 'Practicas'

    def __str__(self):
        return f'{self.student}'
    
class InternshipTracking(TimeStampedBaseModel):
    """ 
    Modelo de seguimiento de práctica, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        observations (TextField): Observaciones
        practice (ForeignKey): Relación con el modelo de `Practice`
    """

    observations = models.TextField(
        max_length = 1000,
        verbose_name = 'Observaciones'
    )
    practice = models.ForeignKey(
        Practice,
        on_delete = models.CASCADE,
        verbose_name = 'Práctica'
    )

    class Meta:
        verbose_name_plural: str = 'Seguimiento de práctica'

    def __str__(self):
        return f'{self.practice}'
    
class DocumentPractice(TimeStampedBaseModel):
    """ 
    Modelo de documentos de práctica, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        name (CharField): Nombre del documento.
        file (FileField): Archivo.
        practice (ForeignKey): Relación con el modelo de `Practice`.
    """

    name = models.CharField(
        max_length = 100,
        verbose_name = 'Nombre'
    )
    file = models.FileField(
        verbose_name = 'Archivo'
    )
    practice = models.ForeignKey(
        Practice,
        on_delete = models.PROTECT,
        verbose_name = 'Práctica'
    )

    class Meta:
        verbose_name_plural: str = 'Documentos de práctica'

    def __str__(self):
        return self.name