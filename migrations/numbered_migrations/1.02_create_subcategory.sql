CREATE TABLE IF NOT EXISTS Subcategory(
    subcategory_id serial PRIMARY KEY,
    name varchar(30),
    category_id serial,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
                        ON DELETE cascade
);