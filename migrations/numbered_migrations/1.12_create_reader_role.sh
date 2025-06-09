#!/bin/bash

PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "CREATE ROLE reader;
                                                    GRANT CONNECT ON DATABASE postgres TO reader;
                                                    GRANT USAGE ON SCHEMA public TO reader;
                                                    GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
                                                    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reader;"
