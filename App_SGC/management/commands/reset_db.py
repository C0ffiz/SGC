import MySQLdb
import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Drops and recreates the database, then runs makemigrations and migrate'

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        conn = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_settings['NAME']}")
        cursor.execute(f"CREATE DATABASE {db_settings['NAME']}")
        self.stdout.write(self.style.SUCCESS('Successfully dropped and recreated the database'))

        # Remove migration files (except __init__.py)
        migrations_dir = os.path.join(settings.BASE_DIR, 'App_SGC', 'migrations')
        for file in glob.glob(os.path.join(migrations_dir, '[!__init__].py')):
            os.remove(file)
        self.stdout.write(self.style.SUCCESS('Removed old migration files'))

        # Run makemigrations and migrate
        self.stdout.write(self.style.SUCCESS('Running makemigrations...'))
        call_command('makemigrations')
        self.stdout.write(self.style.SUCCESS('Running migrate...'))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Successfully ran makemigrations and migrate'))
