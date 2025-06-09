CREATE TABLE IF NOT EXISTS Products(
    product_id serial PRIMARY KEY,
    name TEXT NOT NULL ,
    price serial,
    mass smallserial,
    box_size box_size_kind,
    brand varchar(50),
    subcategory_id serial,
    FOREIGN KEY (subcategory_id) REFERENCES Subcategory(subcategory_id)
        ON DELETE set null ,
    vendor_id serial,
    FOREIGN KEY (vendor_id) REFERENCES Vendor(vendor_id)
        ON DELETE set null ,
    order_id SERIAL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
                     ON DELETE set null

);