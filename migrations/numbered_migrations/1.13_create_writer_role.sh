#!/bin/bash

PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "CREATE ROLE writer;
                                                    GRANT CONNECT ON DATABASE postgres TO writer;
                                                    GRANT USAGE ON SCHEMA public TO writer;
                                                    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO writer;
                                                    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO writer;"
