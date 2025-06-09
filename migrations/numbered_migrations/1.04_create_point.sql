CREATE TABLE IF NOT EXISTS Pick_up_point(
    point_id serial PRIMARY KEY,
    address varchar(100),
    start_daytime time,
    finish_daytime time
);