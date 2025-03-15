from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers.user import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name = _('Email'), unique = True)
    role = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = _('Rol actual'), null = True, blank = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['email']
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        permissions = [
            ('set_password', 'can change the password to other users'),
        ]

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'