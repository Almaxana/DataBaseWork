DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'box_size_kind') THEN
        CREATE type box_size_kind  as enum ('A', 'B', 'C', 'D');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'delivery_status') THEN
        CREATE type delivery_status as enum ('in_stock', 'delivering', 'delivered');
    END IF;
END
$$;



