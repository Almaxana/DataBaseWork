from datetime import datetime
import time
import psycopg2
import os
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
        cursor.execute("SELECT * from users;")
        number_tuples_cur = len(cursor.fetchall())
        number_tuples_need = int(os.environ['DATA_TUPLES_NUMBER'])
        if number_tuples_cur >= number_tuples_need:
            exit()
        else:
            number_tuples_act = number_tuples_need - number_tuples_cur

        fake = Faker(False)
        users = []
        for i in range(0, number_tuples_act):
            user_tuple = (fake.name().split()[0], fake.msisdn()[3:], fake.msisdn()[2:])
            users.append(user_tuple)
            if i%1000 == 0: print(i)
        user_records = ", ".join(["%s"] * len(users))
        insert_query = (
           f"INSERT INTO users (name, phone_number, pay_card_number)  VALUES {user_records}"
        )
        print("start INSERTING into Users")
        cursor.execute(insert_query, users)

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

