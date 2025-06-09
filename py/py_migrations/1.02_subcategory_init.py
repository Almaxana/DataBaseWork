from datetime import datetime
import time
import os
import psycopg2
from psycopg2 import OperationalError
from faker import Faker

def create_connection(db_name, db_user, db_password, db_port, db_host):
    connection = None
    while not connection:
        try:
            connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                port=db_port,
                host=db_host,
            )
            print("Подключение к базе данных PostgreSQL прошло успешно")
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
            time.sleep(3)
    return connection


if __name__ == '__main__':
    time_1 = datetime.now()
    connection = create_connection(
        str(os.environ['POSTGRES_DB']), str(os.environ['POSTGRES_USER']), str(os.environ['POSTGRES_PASSWORD']), "5432", 'db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * from subcategory;")
        number_tuples_cur = len(cursor.fetchall())
        if number_tuples_cur > 0:
            print("everything is up to date in SUBCATEGORY\n")
            exit()

        fake = Faker(False)
        subcategories = [('электрогитары', 2), ('басгитары', 2), ('классические_гитары', 2), ('синтезатор', 1), ('рояль', 1), ('фортепиано', 1),
                         ('синтезатор', 1), ('барабанная_установка', 5), ('барабанные_палочки', 5), ('флейта', 4), ('труба', 4), ('саксофон', 4),
                         ('валторна', 4), ('скрипка', 3), ('альт', 3), ('виолончель', 3), ('контрабас', 3), ('микрофоны', 6)]

        subcategory_records = ", ".join(["%s"] * len(subcategories))
        insert_query = (
           f"INSERT INTO subcategory (name, category_id)   VALUES {subcategory_records}"
        )
        print("start INSERTING")
        cursor.execute(insert_query, subcategories)

        connection.commit()

        time_2 = datetime.now()
        print(time_1)
        print(time_2)
    except SystemExit:
        pass
    except Exception as e:
        connection.rollback()
        print(f"Произошла ошибка '{e}'")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
