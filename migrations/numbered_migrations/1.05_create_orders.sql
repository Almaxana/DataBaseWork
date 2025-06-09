CREATE TABLE IF NOT EXISTS Orders(
    order_id SERIAL PRIMARY KEY,
    status delivery_status,
    user_id serial,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE cascade ,
    destination_id serial,
    FOREIGN KEY (destination_id) REFERENCES Pick_up_point(point_id)
        ON DELETE set null ,
    order_creation_data date,
    delivered_order_data date,
    delivery_price serial
);
