from django.db import models

from core.models import (
    TimeStampedBaseModel
)
from custom_auth.models import (
    CustomUser
)
from companies.models import (
    Company
)
from programs.models import (
    Program,
    Student
)
from .document import (
    DocumentAgreement
)
from .choices import (
    AGREEMENT_CHOICES,
    AGREEMENT_DOCUMENT_CHOICES,
    AGREEMENT_DOCUMENTATION_STATUS,
    AGREEMENT_STUDENT_STATUS,
    AGREEMENT_SCOPE,
    AGREEMENT_TYPES
)

def custom_upload_document(instance, filename):
    try:
        old_instance: AgreementDocumentThrough = AgreementDocumentThrough.objects.get(pk = instance.pk)
        if old_instance.file:
            old_instance.file.delete()
    except AgreementDocumentThrough.DoesNotExist:
        pass
    return f'assets/{instance.agreement.name.replace(" ","_")}/documents/{filename}'

class Agreement(TimeStampedBaseModel):
    """ 
    Modelo de convenios, hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        name (CharField): Nombre del convenio.
        initial_date (DateField): Fecha inicial del convenio.
        end_date (DateField): Fecha finalización del convenio.
        status (CharField): Estado del convenio.
        description (Optional[TextField]): Descripción opcional del convenio.
        requirements (TextField): Requisitos para aplicar al convenio.
        company (ForeignKey): Relación con el modelo `Company`.
        program (ForeignKey): Relación con el modelo `Program`.
        studens (ManyToManyField): Relación de muchos a muchos con el modelo `Student`.
        documents (ManyToManyField): Relación de muchos a muchos con el modelo `DocumentAgreement`.
        agreement_type (CharField): Tipo de convenio. Puede ser:
            - 'ESPECÍFICO' (Específico): Convenios exclusivos para prácticas.
            - 'MACRO' (Macro): Convenios con recursos financieros, becas, estadías, etc.
        scope (CharField): Alcance del convenio. Puede ser:
            - 'NACIONAL' (Nacional): Convenios dentro del país.
            - 'INTERNACIONAL' (Internacional): Convenios con alcance fuera del país.
    """

    name = models.CharField(
        max_length = 200,
        verbose_name = 'Nombre'
    )
    initial_date = models.DateField(
        verbose_name = 'Fecha de inicio'
    )
    end_date = models.DateField(
        verbose_name = 'Fecha de finalización'
    )
    status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado',
        choices = AGREEMENT_CHOICES,
        default = 'INACTIVO'
    )
    description = models.TextField(
        verbose_name = 'Descripción del convenio',
        max_length = 1000,
        null = True,
        blank = True
    )
    documentation_status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado de documentación',
        choices = AGREEMENT_DOCUMENTATION_STATUS,
        default = 'PENDIENTE'
    )
    company = models.ForeignKey(
        Company,
        on_delete = models.PROTECT,
        verbose_name = 'Organización'
    )
    program = models.ForeignKey(
        Program,
        on_delete = models.PROTECT,
        verbose_name = 'Programa'
    )
    students = models.ManyToManyField(
        Student,
        through = 'AgreementStudentThrough',
        blank = True
    )
    documents = models.ManyToManyField(
        DocumentAgreement,
        through = 'AgreementDocumentThrough',
        verbose_name = 'Documentos'
    )
    agreement_type = models.CharField(
        max_length = 100,
        verbose_name = 'Tipo de convenio',
        choices = AGREEMENT_TYPES,
        default = 'ESPECÍFICO'
    )
    scope = models.CharField(
        max_length = 100,
        verbose_name = 'Alcance',
        choices = AGREEMENT_SCOPE,
        default = 'NACIONAL'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Convenios'
        permissions = [
            ('toggle_status', 'Puede cambiar el estado del convenio'),
        ]

    def __str__(self):
        return self.name
    
class AgreementStudentThrough(TimeStampedBaseModel):
    """ 
    Modelo de intermedio entre convenio y estudiante, 
    hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        agreement (ForeignKey): Relación con el modelo `Agreement`.
        student (ForeignKey): Relación con el modelo `Student`.
        status (CharField): Indica el estado del estudiante en el convenio.
    """

    agreement = models.ForeignKey(
        Agreement,
        on_delete = models.CASCADE,
        verbose_name = 'Convenio'
    )
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
        verbose_name = 'Estudiante'
    )
    status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado',
        choices = AGREEMENT_STUDENT_STATUS,
        default = 'ACTIVO'
    )

    def __str__(self):
        return f'{self.agreement} - {self.student}'
    
class AgreementDocumentThrough(TimeStampedBaseModel):
    """ 
    Modelo de intermedio entre convenio y documento convenio
    para la asignación de los documentos requeridos y la subida
    de dichos documentos,hereda de la clase abstracta `TimeStampedBaseModel`

    Inherit:
        TimeStampedBaseModel: Proporciona los Atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de modificación.

    Attributes:
        agreement (ForeignKey): Relación con el modelo `Agreement`.
        document_agreement (ForeignKey): Relación con el modelo `DocumentAgreement`.
        file (FileField): Documento.
        status (CharField): Estado del documento.
        upload_date (DateTimeField): Fecha y hora de subida del documento.
        uploaded_by (CustomUser): Subido por.
    """
    
    agreement = models.ForeignKey(
        Agreement,
        on_delete = models.CASCADE,
        verbose_name = 'Convenio'
    )
    document_agreement = models.ForeignKey(
        DocumentAgreement,
        on_delete = models.CASCADE,
        verbose_name = 'Documento Convenio'
    )
    file = models.FileField(
        verbose_name = 'Archivo',
        null = True,
        blank = True,
        upload_to = custom_upload_document
    )
    status = models.CharField(
        max_length = 100,
        verbose_name = 'Estado',
        default = 'PENDIENTE',
        choices = AGREEMENT_DOCUMENT_CHOICES
    )
    upload_date = models.DateTimeField(
        verbose_name = 'Fecha de subida',
        null = True,
        blank = True
    )
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete = models.PROTECT,
        verbose_name = 'Subido por',
        null = True,
        blank = True
    )

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields = ['agreement', 'document_agreement'],
                name = 'unique_agreement_document'
            )
        ]

    def __str__(self):
        return f'{self.agreement} - {self.document_agreement}'
    
class AgreementDocumentComment(TimeStampedBaseModel):
    """
    Modelo que representa los comentarios y cambios de estado en un documento de convenio.
    Hereda de la clase abstracta `TimeStampedBaseModel`.

    Inherit:
        TimeStampedBaseModel: Proporciona los atributos de marca de tiempo.
            created_at (DateTimeField): Fecha y hora de la creación.
            updated_at (DateTimeField): Fecha y hora de la última modificación.

    Attributes:
        previous_state (CharField): Estado anterior del documento, opcional.
        new_state (CharField): Nuevo estado del documento, obligatorio.
        comment (TextField): Comentario asociado al cambio de estado, con un máximo de 500 caracteres.
        created_by (ForeignKey): Relación con el modelo `CustomUser`, indica quién realizó el comentario o cambio.
        agreement_document (ForeignKey): Relación con el modelo `AgreementDocumentThrough`, representa el documento del convenio afectado.
    """

    previous_state = models.CharField(
        max_length = 100,
        verbose_name = 'Estado anterior',
        choices = AGREEMENT_DOCUMENT_CHOICES,
        null = True
    )
    new_state = models.CharField(
        max_length = 100,
        verbose_name = 'Nuevo estado',
        choices = AGREEMENT_DOCUMENT_CHOICES
    )
    comment = models.TextField(
        max_length = 500,
        verbose_name = 'Comentario'
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete = models.PROTECT,
        verbose_name = 'Creado por'
    )
    agreement_document = models.ForeignKey(
        AgreementDocumentThrough,
        on_delete = models.CASCADE,
        verbose_name = 'Documento del convenio'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural: str = 'Comentarios de documento de convenio'

    def __str__(self):
        return self.new_state
    

class Favoritos(TimeStampedBaseModel):

    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        verbose_name = 'Usuario'
    )
    agreement = models.ForeignKey(
        Agreement,
        on_delete = models.CASCADE,
        verbose_name = 'Convenio'
    )   

    class Meta:
        ordering = ['created_at']
        verbose_name_plural: str = 'Convenios Favoritos'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'agreement'],
                name = 'unique_user_agreement_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.agreement}'