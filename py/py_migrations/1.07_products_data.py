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
        cursor.execute("SELECT * from products;")
        number_tuples_cur = len(cursor.fetchall())
        number_tuples_need = int(os.environ['DATA_TUPLES_NUMBER'])
        print(number_tuples_need)
        if number_tuples_cur >= number_tuples_need:
            exit()
        else:
            number_tuples_act = number_tuples_need - number_tuples_cur

        fake = Faker(False)
        products = []
        music_instrument_provider = DynamicProvider(
         provider_name="music_instrument",
         elements=["IBANEZ GRG121DX-BKF 1", "IBANEZ GRGR131EX-BKF 2", "ROCKDALE STARS HSS BK 3", "IBANEZ GRGR221PA-AQB 4", "IBANEZ GRG121DX-WNF 5", "IBANEZ GIO GRG170DX BKN 6",
                   "ROCKDALE STARS HSS WH 7", "GIBSON SG TRIBUTE VINTAGE CHERRY SATIN 8", "YAMAHA RGX121Z BL 9", "FABIO ST100 BK 10", "SAM MARTIN UP110B 11", "SAMICK JS121MD/WHHP 12", "KAWAI K15E M/ PEP 13", "SAMICK JS118D/WHHP 14",
                   "SAMICK SIG50D/EBHP 15", "KORG PA1000 16", "PEARL RSJ465C/C31 17", "TAMA ST52H6C-BNS STAGESTAR 18", "VIC FIRTH AMERICAN CLASSIC® 5A 1",
                   "STEPHAN WEIS AS-100G 2", "JOHN PACKER JP041 3", "ROY BENSON AS-202A 4", "YAMAHA YFL-212 5", "PEARL QUANTZ PF-F505RE 6",
                   "ARTEMIS RFL-308SEU 7", "FABIO SF3900 N (4/4) 8", "MIRRA VB-290-4/4 9", "GLIGA GENIAL2 B-D034-L 10",
                   ],
        )

        box_category_provider = DynamicProvider(
         provider_name="box_category",
         elements=["A", "B", "C", "D"],
        )

        fake.add_provider(music_instrument_provider)
        fake.add_provider(box_category_provider)

        for i in range (0, number_tuples_act):
            music_instrument_name = fake.music_instrument()
            product_tuple = (music_instrument_name, random.randint(1000, 100000), random.randint(1, 30000),
                             fake.box_category(), music_instrument_name.split()[0], music_instrument_name.split()[-1], random.randint(1, 2),
                             random.randint(1, int(os.environ['DATA_TUPLES_NUMBER'])))
            products.append(product_tuple)
            if i%1000 == 0: print(i)


        product_records = ", ".join(["%s"] * len(products))

        insert_query = (
           f"INSERT INTO products (name, price, mass, box_size, brand, subcategory_id, vendor_id, order_id)  VALUES {product_records}"
        )
        print("start INSERTING into PRODUCTS")
        cursor.execute(insert_query, products)

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
