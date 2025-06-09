from datetime import datetime
import time
import os
import psycopg2
from psycopg2 import OperationalError
from faker import Faker


def create_connection(db_name, db_user, db_password, db_port, db_host):
    # print('category connection')
    connection = None
    while not connection:
        # print("new cycle")
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
            # print("after sleep")
    return connection


if __name__ == '__main__':
    time_1 = datetime.now()
    connection = create_connection(
        str(os.environ['POSTGRES_DB']), str(os.environ['POSTGRES_USER']), str(os.environ['POSTGRES_PASSWORD']), "5432", 'db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * from category;")
        number_tuples_cur = len(cursor.fetchall())
        if number_tuples_cur > 0:
            print("everything is up to date in CATEGORY\n")
            exit()

        fake = Faker(False)
        categories = [('клавишные',), ('струнные',), ('смычковые',), ('духовые',), ('ударные',), ('звуковое_оборудование',)]
        category_records = ", ".join(["%s"] * len(categories))
        insert_query = (
           f"INSERT INTO category (name)  VALUES {category_records}"
        )
        print("start INSERTING")
        cursor.execute(insert_query, categories)

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
            print("category Соединение с PostgreSQL закрыто")
