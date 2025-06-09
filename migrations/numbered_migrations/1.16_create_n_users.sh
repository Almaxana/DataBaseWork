#!/bin/bash
declare -i user_number
for ((i=0;i<$USERS_NUMBER;i++))
do
  echo $user_name
  user_name="user_$i"
  psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "CREATE USER \"$user_name\";
                                                      GRANT group_role TO \"$user_name\";"
done