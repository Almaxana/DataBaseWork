CREATE TABLE IF NOT EXISTS Managers_points(
    manager_id serial,
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
        ON DELETE cascade ,
    point_id serial,
    FOREIGN KEY (point_id) REFERENCES Pick_up_point(point_id)
                            ON DELETE cascade
);