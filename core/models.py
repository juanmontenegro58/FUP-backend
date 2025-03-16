from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class TimeStampedBaseModel(models.Model):
    """ 
    Actúa como una clase base abstracta que proporciona
    los campos 'created_at' y 'updated_at' que se actualizan automáticamente
    en cualquier modelo que herede de ella. 

    Attributes:
        created_at (DateTimeField): Fecha y hora de la creación.
        updated_at (DateTimeField): Fecha y hora de modificación.
    """
    created_at = models.DateTimeField(_('fecha y hora de registro'), auto_now_add=True)
    updated_at = models.DateTimeField(_('última actualización'), auto_now=True)

    class Meta:
        abstract = True

class ContactInfoBaseModel(models.Model):
    """
    Modelo base abstracto que representa la información de contacto.

    Attributes:
        name (str): Mombre.
        phone (str): Número de teléfono.
        email (str): Dirección de correo electrónico.
        address (str): Dirección física.
    """

    name = models.CharField(
        max_length = 255, 
        help_text='Nombre.',
        verbose_name = _('Nombre')
    )
    phone = models.CharField(
        max_length = 20, 
        help_text = 'Número de teléfono.',
        verbose_name = _('Número de teléfono.')
    )
    email = models.EmailField(
        max_length = 255, 
        unique = True,
        help_text = 'Dirección de correo electrónico.',
        verbose_name = _('Dirección de correo electrónico')
    )
    address = models.CharField(
        max_length = 500,
        help_text='La dirección física.',
        verbose_name = _('La dirección física.')
    )

    class Meta:
        abstract = True