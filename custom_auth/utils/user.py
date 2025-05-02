from typing import (
    Dict,
    Any
)

from django.db.models import Model

from programs.models import Student
from evaluations.models import Teacher
from companies.models import Company

def find_user_info_by_document(
    document_number: str,
    full_info: bool = False
) -> Dict[str, Any]:
    FIELDS_TO_GET = {
        'first_name': ['first_name', 'second_name'],
        'last_name': ['first_surname', 'second_surname'],
    }
    MODELOS_BUSQUEDA = [
        {
            'model': Student,
            'field': 'document_number',
            'role': 'ESTUDIANTE',
            'fields_to_get': FIELDS_TO_GET,
        },
        {
            'model': Teacher,
            'field': 'document_number',
            'role': 'DOCENTE',
            'fields_to_get': FIELDS_TO_GET
        },  
        # {
        #     'model': Company,
        #     'field': 'nui',
        #     'role': 'EMPRESA',
        #     'fields_to_get': {
        #         'first_name': ['name']
        #     }
        # },
    ]

    instance = None
    role = None
    fields = {}
    user_data = {}

    for config in MODELOS_BUSQUEDA:
        model: Model = config['model']
        filters = {config['field']: document_number}
        instance = model.objects.filter(**filters).first()

        if instance:
            fields = config['fields_to_get']
            role = config['role']
            break
    if not role:
        return {'valid': False, 'detail': 'No se encontró ningún registro asociado'}

    if full_info:
        for field_key, field in fields.items():
            value = ' '.join(getattr(instance, f) for f in field if getattr(instance, f)).strip().capitalize()
            user_data[field_key] = value
        return {
            'valid': True,
            'role': role,
            'data': user_data,
            'instance': instance
        }
    return {
        'valid': True
    }