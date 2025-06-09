import random
from faker import Faker
import time
import os
import psycopg2
from psycopg2 import OperationalError


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
    time = str(time.time())
    connection = create_connection(
        str(os.environ['POSTGRES_DB']), str(os.environ['POSTGRES_USER']), str(os.environ['POSTGRES_PASSWORD']), "5432", 'db')
    starts_for_one_query = int(os.environ['EXPLAIN_START_QUERIES_NUMBER'])

    cursor = connection.cursor()

    queries = []

    query_1 = """SELECT products.name FROM products
JOIN subcategory ON products.subcategory_id = subcategory.subcategory_id
JOIN product_review ON products.product_id = product_review.product_id
WHERE subcategory.name = 'электрогитары' AND products.brand = 'IBANEZ'
GROUP BY products.name
HAVING avg(product_review.rating) > {}"""

    query_2 = """SELECT * FROM orders
WHERE order_creation_data >= '{}'"""

    query_3 = """SELECT year, month, avg(sum) FROM
                       (SELECT EXTRACT(YEAR FROM order_creation_data) AS year, EXTRACT(MONTH FROM order_creation_data) AS month, sum(products.price) AS sum FROM orders
                        JOIN products ON products.order_id = orders.order_id
                        WHERE order_creation_data >= '{}'
                        GROUP BY year, month, orders.order_id)
GROUP BY year, month"""

    query_4 = """SELECT * FROM orders
WHERE user_id = '{}'"""

    query_5 = """SELECT * FROM
             (SELECT category.name AS category_name, subcategory.name, ROW_NUMBER() OVER (PARTITION BY category.name ORDER BY count(*) DESC) AS rnk FROM products
            JOIN subcategory ON products.subcategory_id = subcategory.subcategory_id
            JOIN category ON subcategory.category_id = category.category_id
            WHERE order_id IS NOT NULL
            GROUP BY category.name, subcategory.name
            )
WHERE rnk <=3"""

    queries.append(query_1)
    queries.append(query_2)
    queries.append(query_3)
    queries.append(query_4)
    queries.append(query_5)

    fake = Faker(False)

    try:
        query_number = 0
        for query in queries:
            query_number+=1
            query_times = []
            for number_start in range(0, starts_for_one_query):
                if query_number == 1:
                    query = query.format(str(random.uniform(0.1, 5.0)))
                elif query_number == 2 or query_number == 3:
                    query = query.format(str(fake.date(pattern="%Y-%m-%d", end_datetime=None)))
                elif query_number == 4:
                    query = query.format(str(random.randint(1, int(os.environ['DATA_TUPLES_NUMBER']))))
                actual_time = None
                cursor.execute("EXPLAIN ANALYSE " + query)
                for row in cursor:
                    for part in row[0].split():
                        if part.startswith("time"):
                            actual_time = float(part.split("..")[1])
                            break
                    query_times.append(actual_time)
                    print(actual_time)
                    break

            cursor.execute("EXPLAIN ANALYSE " + query)
            for row in cursor:
                for part in row[0].split():
                    if part.startswith("(cost"):
                        cost = float(part.split("..")[1])
                        break

            query_times.sort()
            min_time = min(query_times)
            max_time = max(query_times)
            mid_time = sum(query_times)/len(query_times)
            print(min_time, mid_time, max_time, cost)
            with open('./queries_results/query_report_' + time, 'a') as file:
                file.write(str(query_number) + ' ')
                file.write(str(min_time) + " ")
                file.write(str(mid_time) + " ")
                file.write(str(max_time) + " ")
                file.write(str(cost) + " \n")

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Произошла ошибка '{e}'")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("category Соединение с PostgreSQL закрыто")
