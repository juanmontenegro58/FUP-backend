from django.db.models.signals import (
    post_save,
    m2m_changed
)
from django.dispatch import receiver
from ..models import (
    AgreementDocumentThrough,
    Agreement
)

def update_documentation_status(agreement: Agreement):
    """ 
    Actualiza el estado de la documentación del convenio.
        - `COMPLETA` -> Si todos los documentos están cargados y 
            aprobados.
        - `INCOMPLETA` -> Si hay al menos un documento subido pero 
            no todos se han cargado o no están aprobados.

    Params:
        agreement (Agreement): Instancia del convenio.
    """
    
    documents = agreement.agreementdocumentthrough_set.all()

    if all(doc.status == 'APROBADO' for doc in documents):
        new_documentation_status = 'COMPLETA'
        new_status = 'ACTIVO'
    elif any(doc.file for doc in documents):
        new_status = 'INACTIVO'
        new_documentation_status = 'INCOMPLETA'
    else:
        return
    if agreement.documentation_status != new_documentation_status:
        agreement.documentation_status = new_documentation_status
        agreement.save(update_fields = ['documentation_status'])
    if agreement.status != new_status:
        agreement.status = new_status
        agreement.save(update_fields = ['status'])

@receiver(post_save, sender = AgreementDocumentThrough)
def agreement_document_through_signal(sender, instance, **kwargs):
    update_documentation_status(
        agreement = instance.agreement
    )

@receiver(m2m_changed, sender=AgreementDocumentThrough)
def convenio_documents_changed(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_documentation_status(
            agreement = instance
        )
