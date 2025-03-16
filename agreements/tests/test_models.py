from datetime import datetime

from django.test import TestCase

from ..models import (
    Agreement,
    DocumentAgreement,
    AgreementDocumentThrough,
    AgreementStudentThrough
)
from programs.models import (
    Student,
    Program
)
from companies.models import (
    Company
)

class AgreementModelTest(TestCase):
    
    def setUp(self):
        data = {
            'name': 'Tech Corp',
            'phone': '3012342340',
            'email': 'email@email.com',
            'address': 'CL 46 N # 9AN',
            'nui': '9099900000'
        }
        self.company = Company.objects.create(**data)
        self.program = Program.objects.create(
            name = 'Ingenieria de sistemas',
            code = 1234567
        )
        self.agreement = Agreement.objects.create(
            name = 'Convenio X',
            initial_date = datetime.now().date(),
            end_date = datetime.strptime('2026-12-12', '%Y-%m-%d').date(),
            requirements = 'Estos son los requerimientos para aplicar',
            company = self.company,
            program = self.program
        )

    def test_create_agreement(self):
        """ Verifica que se pueda crear un convenio """
        data = {
            'name': 'Convenio X',
            'initial_date': datetime.now().date(),
            'end_date': datetime.strptime('2026-12-12', '%Y-%m-%d').date(),
            'requirements': 'Estos son los requerimientos para aplicar',
            'company': self.company,
            'program': self.program
        }
        agreement = Agreement.objects.create(**data)
        self.assertEqual(agreement.name, data['name'])
        self.assertEqual(agreement.status, 'INACTIVO')
        self.assertEqual(agreement.company.name, self.company.name)
        self.assertEqual(agreement.program.name, 'Ingenieria de sistemas')

    def test_associtate_document_to_agreement(self):
        """ Verifica que se puedan asociar multiples documentos a un convenio. """
        documents = [
            DocumentAgreement.objects.create(
                name = 'Certificado Antecedentes Policia',
                description = 'Certificado Antecedentes Policia',
            ),
            DocumentAgreement.objects.create(
                name = 'Certificado Antecedentes Contraloria',
                description = 'Certificado Antecedentes Contraloria',
            )
        ]

        self.agreement.documents.add(*documents)

        self.assertEqual(self.agreement.documents.all().count(), len(documents))

    def test_associate_student_to_agreement(self):
        """ Verifica que se pueden asociar multiples estudiantes a un convenio. """

        students = [
            Student.objects.create(
                first_name = 'Wally',
                first_surname = 'West',
                code = 71449983,
                document_number = '108387493',
                email = 'student@email.com',
                program = self.program
            ),
            Student.objects.create(
                first_name = 'Tony',
                first_surname = 'Dinozzo',
                code = 7183940,
                document_number = '109384773',
                email = 'tony@email.com',
                program = self.program
            ),
        ]

        self.agreement.students.add(*students)

        self.assertEqual(self.agreement.students.all().count(), len(students))
