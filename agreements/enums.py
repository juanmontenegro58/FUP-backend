from enum import Enum

class AgreementDocumentationStatusEnum(Enum):
    PENDIENTE = 'PENDIENTE'
    INCOMPLETA = 'INCOMPLETA'
    COMPLETA = 'COMPLETA'
    
class AgreementDocumentStatusEnum(Enum):
    PENDIENTE = 'PENDIENTE'
    SUBIDO = 'SUBIDO'
    APROBADO = 'APROBADO'
    RECHAZADO = 'RECHAZADO'