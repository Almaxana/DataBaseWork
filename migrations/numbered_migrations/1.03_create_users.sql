CREATE TABLE IF NOT EXISTS Users(
    user_id serial PRIMARY KEY ,
    phone_number varchar(11),
    name varchar(50),
    pay_card_number varchar(20)
);