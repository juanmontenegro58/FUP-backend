from django.contrib import admin

from .models import (
    Program
)

# Register your models here.

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    ...