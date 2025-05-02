from django.db import models

from core.models import (
    TimeStampedBaseModel
)
from programs.models import (
    Student
)
from agreements.models import (
    Agreement
)

class PracticalOffer(TimeStampedBaseModel):
    """ 
    Modelo de ofertas prácticas, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        title (CharField): Título de la oferta.
        description (TextField): Descripción de la oferta.
        agreement (ForeignKey): Relación con el modelo de `Agreement`.
        students (ManyToManyField): Relación muchos a muchos con el modelo `Student`.
        vacancies (PositiveIntegerField): Número de vacantes disponibles.
        close_date (DateField): Fecha de cierre de la oferta.
        skills (TextField): Habilidades requeridas.
        responsibilities (TextField): Responsabilidades del practicante.
    """

    title = models.CharField(
        max_length = 100,
        verbose_name = 'Titulo'
    )
    description = models.TextField(
        max_length = 2000,
        verbose_name = 'Descripción'
    )
    agreement = models.ForeignKey(
        Agreement,
        on_delete = models.PROTECT,
        verbose_name = 'Convenio'
    )
    students = models.ManyToManyField(
        Student,
        through = 'PracticalOfferStudentThrough',
        blank = True
    )
    skills = models.TextField(
        verbose_name='Habilidades'
    )
    responsibilities = models.TextField(
        verbose_name='Responsabilidades'
    )
    close_date = models.DateField(
        verbose_name='Fecha de cierre'
    )
    vacancies = models.PositiveIntegerField(
        default=1, 
        verbose_name='Vacantes'
    )

    class Meta:
        verbose_name: str = 'Oferta práctica'
        verbose_name_plural: str = 'Ofertas practicas'

    def __str__(self):
        return self.title
    
class PracticalOfferStudentThrough(TimeStampedBaseModel):
    """ 
    Modelo intermedio entre ofertas prácticas y estudiante, 
    hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        practical_offer (ForeignKey): Relación con el modelo de `PracticalOffer`.
        student (ForeignKey): Relación con el modelo de `Student`.
        status (CharField): Estado de la aplicación a la oferta.
    """

    practical_offer = models.ForeignKey(
        PracticalOffer,
        on_delete = models.CASCADE,
        verbose_name = 'Oferta práctica'
    )
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
        verbose_name = 'Estudiante'
    )
    status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado' 
    )

    def __str__(self):
        return f'{self.practical_offer} - {self.student}'