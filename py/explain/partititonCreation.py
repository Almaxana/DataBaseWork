import time
import os
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_port, db_host):
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
    return connection


if __name__ == '__main__':
    time = str(time.time())
    connection = create_connection(
        str(os.environ['POSTGRES_DB']), str(os.environ['POSTGRES_USER']), str(os.environ['POSTGRES_PASSWORD']), "5432", 'db')
    starts_for_one_query = int(os.environ['EXPLAIN_START_QUERIES_NUMBER'])

    cursor = connection.cursor()


    try:
        cursor.execute("CREATE TABLE orders_partitioned (LIKE orders) PARTITION BY RANGE (order_creation_data)")
        for year in range(10, 25):
                cursor.execute("CREATE TABLE orders{} PARTITION OF orders_partitioned FOR VALUES FROM ('{}') TO ('{}')".format(year, '20'+str(year)+'-01-01', '20'+str(year+1)+'-01-01'))
        cursor.execute("INSERT INTO orders_partitioned SELECT * FROM orders;")
        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Произошла ошибка '{e}'")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("category Соединение с PostgreSQL закрыто")
