import random
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
        cursor.execute("SELECT * from product_review;")
        number_tuples_cur = len(cursor.fetchall())
        number_tuples_need = int(os.environ['DATA_TUPLES_NUMBER'])
        if number_tuples_cur >= number_tuples_need:
            exit()
        else:
            number_tuples_act = number_tuples_need - number_tuples_cur

        fake = Faker(False)
        review_content_provider = DynamicProvider(
         provider_name="review_content",
         elements=['good product i think', 'i would not recommend this instrument because i dont like it', 'some review text text text text text text'],
        )

        fake.add_provider(review_content_provider)

        reviews = []
        for i in range (0, number_tuples_act):
            order_tuple = (fake.review_content(), '2024-06-07 '+ str(random.randint(10, 23)) +':' + str(random.randint(10, 59))+':33', random.randint(1, int(os.environ['DATA_TUPLES_NUMBER'])), random.randint(1, int(os.environ['DATA_TUPLES_NUMBER'])), random.uniform(0.1, 4.9))
            reviews.append(order_tuple)
            if i%1000 == 0: print(i)

        reviews_records = ", ".join(["%s"] * len(reviews))
        insert_query = (
           f"INSERT INTO product_review (content, creation_data, product_id, user_id, rating)   VALUES {reviews_records}"
        )
        print("start INSERTING into REVIEW")
        cursor.execute(insert_query, reviews)

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
