from datetime import datetime
import time
import psycopg2
import os
import random
from psycopg2 import OperationalError
from faker import Faker
from faker.providers import DynamicProvider

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
        cursor.execute("SELECT * from orders;")

        number_tuples_cur = len(cursor.fetchall())
        number_tuples_need = int(os.environ['DATA_TUPLES_NUMBER'])
        if number_tuples_cur >= number_tuples_need:
            exit()
        else:
            number_tuples_act = number_tuples_need - number_tuples_cur


        fake = Faker(False)
        orders = []


        delivery_status_provider = DynamicProvider(
         provider_name="delivery_status",
         elements=['in_stock', 'delivering', 'delivered'],
        )

        fake.add_provider(delivery_status_provider)

        for i in range (0, number_tuples_act):
            year = str(random.randint(10, 24))
            month = str(random.randint(1, 8))
            next_month = str(int(month) + 1)

            order_tuple = (fake.delivery_status(), random.randint(1, int(os.environ['DATA_TUPLES_NUMBER'])), random.randint(1, 2),
                           '20' + year +'-0' + month + '-' + str(random.randint(10, 23)), '20' + year +'-0'+ next_month + '-' + str(random.randint(10, 28)), random.randint(500, 3000) )
            orders.append(order_tuple)
            if i%1000 == 0: print(i)

        order_records = ", ".join(["%s"] * len(orders))

        insert_query = (
           f"INSERT INTO orders (status, user_id, destination_id, order_creation_data, delivered_order_data, delivery_price)   VALUES {order_records}"
        )
        print("start INSERTING into ORDERS")
        cursor.execute(insert_query, orders)

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
