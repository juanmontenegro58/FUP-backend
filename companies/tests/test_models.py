from django.test import TestCase
from django.db import IntegrityError

from ..models import (
    Company,
    Contact
)

class CompanyModelTest(TestCase):

    def test_create_company(self):
        """Verifica que se puede crear una compañía correctamente."""
        data = {
            'name': 'Tech Corp',
            'phone': '3012342340',
            'email': 'email@email.com',
            'address': 'CL 46 N # 9AN',
            'nui': '9099900000'
        }
        company = Company.objects.create(**data)
        self.assertEqual(company.name, data['name'])
        self.assertIsNotNone(company.created_at)

    def test_unique_company_nui(self):
        """Verifica que el nombre de la compañía debe ser único."""
        data = {
            'name': 'Tech Corp',
            'phone': '3012342340',
            'email': 'email@email.com',
            'address': 'CL 46 N # 9AN',
            'nui': '9099900000'
        }
        Company.objects.create(**data)
        with self.assertRaises(IntegrityError):
            Company.objects.create(**data)

class ContactModelTest(TestCase):
    
    def setUp(self):
        self.company_data = {
            'name': 'Tech Corp',
            'phone': '3012342340',
            'email': 'email@email.com',
            'address': 'CL 46 N # 9AN',
            'nui': '9099900000'
        }
        self.company = Company.objects.create(**self.company_data)

    def test_create_contact(self):
        """Verifica que se puede crear un contacto asociado a una compañía."""
        data = {
            'name': 'Barry Allen',
            'phone': '3010000000',
            'email': 'barry@email.com',
            'address': 'CL 46 N # 9AN',
            'company': self.company
        }
        contact = Contact.objects.create(**data)
        self.assertEqual(contact.name, data['name'])
        self.assertEqual(contact.company.name, self.company_data['name'])

    def test_unique_email(self):
        """Verifica que no se pueden registrar dos contactos con el mismo email."""
        data = {
            'name': 'Barry Allen',
            'phone': '3010000000',
            'email': 'barry@email.com',
            'address': 'CL 46 N # 9AN',
            'company': self.company
        }
        Contact.objects.create(**data)
        with self.assertRaises(IntegrityError):
            Contact.objects.create(**data)

    def test_delete_company_deletes_contacts(self):
        """Verifica que al eliminar una compañía, sus contactos también se eliminan (on_delete=models.CASCADE)."""
        data = {
            'name': 'Barry Allen',
            'phone': '3010000000',
            'email': 'barry@email.com',
            'address': 'CL 46 N # 9AN',
            'company': self.company
        }
        Contact.objects.create(**data)
        self.company.delete()
        self.assertEqual(Contact.objects.count(), 0)