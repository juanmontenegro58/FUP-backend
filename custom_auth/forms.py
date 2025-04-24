from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
)
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """ Formulario personalizado para la creación de un usuario. """
    first_name = forms.CharField(
        label = _('Nombres'),
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'vTextField'}
        )
    )
    last_name = forms.CharField(
        label = _('Apellidos'),
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'vTextField'}
        )
    )
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        users_with_email = get_user_model().objects.filter(email = email)
        if users_with_email.exists():
            raise forms.ValidationError(_('Este email ya se encuentra registrado'))
        return email

class CustomUserChangeForm(UserChangeForm):
    """ Formulario personalizado para editar un usuario. """
    
    first_name = forms.CharField(
        label = _('Nombres'),
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'vTextField'}
        )
    )
    last_name = forms.CharField(
        label = _('Apellidos'),
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'vTextField'}
        )
    )
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']