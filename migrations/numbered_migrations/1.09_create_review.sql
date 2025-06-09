CREATE TABLE IF NOT EXISTS Product_review(
    review_id serial PRIMARY KEY,
    user_id serial,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE set null ,
    content text,
    product_id serial,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
        ON DELETE cascade ,
    creation_data timestamp,
    rating float check (rating between 0 and 5)
);