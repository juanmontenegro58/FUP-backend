from django.contrib import admin

from .models import (
    Agreement,
    DocumentAgreement
)

# Register your models here.

class AgreementDocumentThroughInline(admin.TabularInline):
    model = Agreement.documents.through
    extra: int = 1
    min_num: int = 1

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    
    inlines = [
        AgreementDocumentThroughInline
    ]

@admin.register(DocumentAgreement)
class DocumentAgreementAdmin(admin.ModelAdmin):
    ...