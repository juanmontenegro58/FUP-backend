from django.contrib import admin

from .models import (
    Company,
    Contact
)

# Register your models here.
class ContactInline(admin.TabularInline):
    model = Contact
    min_num: int = 1
    extra: int = 1 

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline
    ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    ...