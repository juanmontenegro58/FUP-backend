from django.contrib import admin

from .models import (
    Program,
    Student
)

# Register your models here.

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    ...

admin.site.register(Student)