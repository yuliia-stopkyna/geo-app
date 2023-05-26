import os
from time import sleep

import psycopg2
from dotenv import load_dotenv

from django.core.management.base import BaseCommand

load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            psycopg2.connect(
                f"dbname={os.getenv('POSTGRES_DB')} "
                f"user={os.getenv('POSTGRES_USER')} "
                f"password={os.getenv('POSTGRES_PASSWORD')} "
                f"host={os.getenv('POSTGRES_HOST')}"
            )
        except psycopg2.OperationalError:
            sleep(5)
            self.handle(*args, **options)
        else:
            self.stdout.write(
                self.style.SUCCESS("Connection to database established")
            )
