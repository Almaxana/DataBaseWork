#!/bin/bash

last_migration_number_str=$LAST_MIGRATION_NUMBER
if [[ -z "$last_migration_number_str" ]]
then
  last_migration_number=-1
else
  last_migration_number=$(awk "BEGIN{print $last_migration_number_str}")
fi

for migration_file in  /numbered_migrations/*
do
  migration_number_str=$(echo $(echo $migration_file | awk -F/ '{print $3}') | awk -F_ '{print $1}')
  migration_number=$(awk "BEGIN{print $migration_number_str}")

  file_extension=$(echo $migration_file | awk -F. '{print $3}')

  if [[ $last_migration_number != -1 ]]
  then
    if [[ $migration_number < $last_migration_number ]]
    then
      if [[ $file_extension == "sql" ]]
      then
        PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -f $migration_file
      else
        bash $migration_file
      fi
    fi
  else
    if [[ $file_extension == "sql" ]]
      then
        PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -f $migration_file
      elif [[ $file_extension == "py" ]]
      then
        /usr/bin/python3 $migration_file
      else
        bash $migration_file
      fi
  fi

done