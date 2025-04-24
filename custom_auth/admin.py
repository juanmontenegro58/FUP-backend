from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm
)

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'is_active')
    ordering = ('email',)
    readonly_fields = ('last_login','date_joined')
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    search_fields = ['email']

    add_fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
            ),
        }),
        ('Permisos', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
    )
    fieldsets = (
         (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password',
            ),
        }),
        ('Permisos', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Fechas importantes', 
            {'fields': 
                ('last_login', 'date_joined')
            }
        )
    )