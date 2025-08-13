import psycopg2
from decouple import config
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dbname = config('NAME')
user = config('USER')
password = config('PASSWORD')
host = config('HOST')
port = config('PORT')


class Command(BaseCommand):
    help = 'Проверка существования БД. Если нет - создает'

    def handle(self, *args, **options):

        def create_database():
            conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f'CREATE DATABASE {dbname};')
            cur.close()
            conn.close()

        def check_exist():
            try:
                conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
                conn.close()
                print(f'База данных "{dbname}" существует и доступна.')
            except (OperationalError, UnicodeDecodeError):
                print(f'База данных "{dbname}" не найдена. Создаём...')
                create_database()
                print(f'База данных {dbname} создана.')

        check_exist()
