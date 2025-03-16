from django.test import TestCase
from django.db import IntegrityError

from ..models import (
    Program,
    Student
)

class ProgramModelTest(TestCase):

    def setUp(self):
        data = {
            'name': 'Ingenieria de sistemas',
            'code': 1223444
        }
        self.program = Program.objects.create(**data)
    
    def test_create_program(self):
        """ Prueba para verificar que se pueda crear un programa. """
        data = {
            'name': 'Ingenieria de electronica',
            'code': 12023444
        }
        program = Program.objects.create(**data)

        self.assertEqual(program.name, data['name'])
        self.assertEqual(program.code, data['code'])

    def test_update_program(self):
        """ Verifica la acutalización de un programa """
        new_program_name = 'Ingenieria Informatica'
        new_code = 109999999

        self.program.name = new_program_name
        self.program.code = new_code
        self.program.save()

        program_update = Program.objects.get(pk = self.program.pk)

        self.assertEqual(program_update.name, new_program_name)
        self.assertEqual(program_update.code, new_code)

    def test_list_programs(self):
        """ Verifica que se puedan listar programas """
        data = {
            'name': 'Ingenieria de ambiental',
            'code': 17223444
        }
        Program.objects.create(**data)

        programs = Program.objects.all()
        self.assertEqual(programs.count(), 2)

    def test_unique_code(self):
        """ Verifica que se creen programas con datos (name, code) únicos. """
        data = {
            'name': 'Ingenieria Industrial',
            'code': 12234454
        }
        Program.objects.create(**data)
        with self.assertRaises(IntegrityError):
            Program.objects.create(**data)

class StudentModelTest(TestCase):

    def setUp(self):
        self.program = Program.objects.create(
            name = 'Ingenieria de Software',
            code = 1234567
        )

    def test_create_student(self):
        """ Verifica que se pueda crear un estudiante. """
        data = {
            'first_name': 'Wally',
            'first_surname': 'West',
            'code': 71449983,
            'document_number': '108387493',
            'email': 'wally@email.com',
            'program': self.program
        }
        student = Student.objects.create(**data)

        self.assertEqual(student.first_name, data['first_name'])
        self.assertIsNone(student.second_name)
        self.assertEqual(student.first_surname, data['first_surname'])
        self.assertIsNone(student.second_surname)
        self.assertEqual(student.code, data['code'])
        self.assertEqual(student.document_number, data['document_number'])
        self.assertEqual(student.email, data['email'])
        self.assertEqual(student.program.name, self.program.name)

    def test_update_student(self):
        """ Verifica que la información del estudiante se pueda actualizar. """
        data = {
            'first_name': 'Wally',
            'first_surname': 'West',
            'code': 71449983,
            'document_number': '108387493',
            'email': 'west@email.com',
            'program': self.program
        }
        second_name = 'Anthony'
        student = Student.objects.create(**data)

        student.second_name = second_name
        student.save()

        student = Student.objects.get(pk = student.pk)
        self.assertEqual(student.second_name, second_name)

    def test_list_students(self):
        """ Verifica que se puedan listar los estudiantes """
        students = []
        for item in range(2):
            data = {
                'first_name': 'Wally',
                'first_surname': 'West',
                'code': int(f'{item}71449983'),
                'document_number': f'{item}108387493',
                'email': f'{item}student@email.com',
                'program': self.program
            }
            students.append(Student.objects.create(**data))

        students_db = Student.objects.all()
        self.assertEqual(students_db.count(), len(students))

    def test_unique_email_code_for_student(self):
        data = {
            'first_name': 'Wally',
            'first_surname': 'West',
            'code': 71449983,
            'document_number': '108387493',
            'email': 'iris@email.com',
            'program': self.program
        }
        Student.objects.create(**data)
        with self.assertRaises(IntegrityError):
            Student.objects.create(**data)
