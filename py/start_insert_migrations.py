import time
import os.path

if __name__ == '__main__':
    print("START MIGRATIONS")
    if os.environ['LAST_MIGRATION_NUMBER'] != '':
        lastMigration = float(os.environ['LAST_MIGRATION_NUMBER'])
    else:
        lastMigration = -1

    folder_path = 'py_migrations'
    files_in_order = []
    for file_name in os.listdir(folder_path):
        files_in_order.append(file_name)
    files_in_order.sort()

    for file_name in files_in_order:
        migration_number = float(file_name.split('_')[0])
        if lastMigration != -1 and migration_number > lastMigration:
            break
        exec(open('py_migrations/' + file_name).read())
    while True:
        time.sleep(30)
