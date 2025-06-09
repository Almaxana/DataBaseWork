#!/bin/bash

PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "CREATE ROLE group_role;
                                                    GRANT CONNECT ON DATABASE postgres TO group_role;
                                                    GRANT USAGE ON SCHEMA public TO group_role;
                                                    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO group_role;
                                                    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO group_role;"
