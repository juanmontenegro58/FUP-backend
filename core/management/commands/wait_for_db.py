from time import sleep

from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Waiting for database...'))        
        conected = False
        while not conected:
            try:
                connection.ensure_connection()
                conected = True
            except OperationalError:
                self.stdout.write(self.style.WARNING('Database unavailable, waiting 2 second...'))
                sleep(2)
        self.stdout.write(self.style.SUCCESS('Database available!'))