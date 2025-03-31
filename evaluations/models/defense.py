from django.db import models

from custom_auth.models import (
    CustomUser
)
from core.models import (
    TimeStampedBaseModel
)
from .choices import (
    DEFENSE_STATUS_CHOICES,
    DEFENSE_RESULT_CHOICES,
    DEFENSE_TEACHER_ROLE_CHOICES
)
from programs.models import (
    Student
)
from .teacher import (
    Teacher
)

class Defense(TimeStampedBaseModel):
    """ 
    Modelo de sustentación, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        application_date (DateField): Fecha de solicitud.
        scheduled_date (DateField): Fecha programada.
        status (CharField): Estado de la sustentación.
        result (CharField): Resultado final de la sustentación.
        students (ManyToManyField): Relación de muchos a muchos con el modelo `Student`.
        teachers (ManyToManyField): Relación de muchos a muchos con el modelo `Teacher`.
    """

    application_date = models.DateField(
        verbose_name = 'Fecha de solicitud',
    )
    scheduled_date = models.DateField(
        verbose_name = 'Fecha programada'
    )
    status = models.CharField(
        max_length = 100,
        default = 'PENDIENTE',
        choices = DEFENSE_STATUS_CHOICES,
        verbose_name = 'Estado'
    )
    result = models.CharField(
        max_length = 100,
        verbose_name = 'Resultado final',
        choices = DEFENSE_RESULT_CHOICES,
        default = 'N/A'
    )
    students = models.ManyToManyField(
        Student,
        through = 'DefenseStudentThrough'
    )
    teachers = models.ManyToManyField(
        Teacher,
        through = 'DefenseTeacherThrough'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Sustentaciones'

    def __str__(self):
        return str(self.scheduled_date)
    
class DefenseStudentThrough(TimeStampedBaseModel):
    """ 
    Modelo intermedio entre sustentación y estudiante, 
    hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        defense (ForeignKey): Relación con el modelo `Defense`.
        student (ForeignKey): Relación con el modelo `Student`.
    """

    defense = models.ForeignKey(
        Defense,
        on_delete = models.CASCADE,
        verbose_name = 'Sustentación'
    )
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
        verbose_name = 'Estudiante'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.defense} - {self.student}'

class DefenseTeacherThrough(TimeStampedBaseModel):
    """ 
    Modelo intermedio entre sustentación y docente, 
    hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        defense (ForeignKey): Relación con el modelo `Defense`.
        teacher (ForeignKey): Relación con el modelo `Teacher`.
        role (CharField): Rol del docente en la sustentación
    """

    defense = models.ForeignKey(
        Defense,
        on_delete = models.CASCADE,
        verbose_name = 'Sustentación'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete = models.CASCADE,
        verbose_name = 'Docente'
    )
    role = models.CharField(
        max_length = 100,
        verbose_name = 'Rol del docente',
        choices = DEFENSE_TEACHER_ROLE_CHOICES
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.teacher} - {self.defense}'
    
class DefenseComment(TimeStampedBaseModel):
    """
    Modelo que representa los comentarios realizados en una sustentación.
    Hereda de la clase abstracta `TimeStampedBaseModel`.

    Inherit:
        TimeStampedBaseModel: Proporciona los atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de la última modificación.

    Attributes:
        comment (TextField): Contenido del comentario, con un máximo de 500 caracteres.
        created_by (ForeignKey): Relación con el modelo `CustomUser`, indica quién creó el comentario.
        defense (ForeignKey): Relación con el modelo `Defense`, representa la sustentación a la que pertenece el comentario.
    """

    comment = models.TextField(
        max_length = 500,
        verbose_name = 'Comentario'
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete = models.PROTECT,
        verbose_name = 'Creado por'
    )
    defense = models.ForeignKey(
        Defense,
        on_delete = models.CASCADE,
        verbose_name = 'Sustentación'
    )
    previous_date = models.DateField(
        verbose_name="Fecha anterior",
        blank=True,
        null=True
    )
    new_date = models.DateField(
        verbose_name="Nueva fecha",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural: str = 'Comentarios de sustentación'

    def __str__(self):
        return self.comment