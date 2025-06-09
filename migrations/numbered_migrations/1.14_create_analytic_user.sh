#!/bin/bash

PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "CREATE USER analytic WITH PASSWORD 'analytic_psswd';
                                                    GRANT CONNECT ON DATABASE postgres TO analytic;
                                                    GRANT USAGE ON SCHEMA public TO analytic;
                                                    GRANT SELECT ON TABLE users TO analytic;"
