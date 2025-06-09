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
        cursor.execute("SELECT * from manager;")
        number_tuples_cur = len(cursor.fetchall())
        if number_tuples_cur > 0:
            exit()

        fake = Faker(False)
        managers = [('89022445761', 'Петя'), ('89022820761', 'Вова')]

        managers_records = ", ".join(["%s"] * len(managers))

        insert_query = (
           f"INSERT INTO manager (phone_number, name)   VALUES {managers_records}"
        )
        print("start INSERTING")
        cursor.execute(insert_query, managers)

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
