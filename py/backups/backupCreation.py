import schedule
import subprocess
import time
from datetime import datetime
import os
def backup_database(database_name, username, password, host, port, filename, backups_number):
    folder_path = 'backups/saved_backups/'
    files_in_order = []
    for file_name in os.listdir(folder_path):
        files_in_order.append(file_name)
    if backups_number - len(files_in_order) < 1:
        files_in_order.sort()
        os.remove(folder_path + files_in_order[0])
    print(files_in_order)
    command = f"PGPASSWORD={password} pg_dumpall -U {username} -h {host} -p {port} > {filename}"


    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode == 0:
        print(f"Резервная копия базы данных '{database_name}' успешно создана: {filename}")
    else:
        print(f"Ошибка при создании резервной копии: {process.returncode}")

if __name__ == '__main__':
    print("backup creation started")

    schedule.every(60*int(os.environ['BACKUPS_INTERVAL'])).minutes.do(backup_database, str(os.environ['POSTGRES_DB']), str(os.environ['POSTGRES_USER']), str(os.environ['POSTGRES_PASSWORD']), 'db', "5432", 'backups/saved_backups/backup_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.sql', int(os.environ['BACKUPS_NUMBER']))

    while True:
        schedule.run_pending()
        time.sleep(1)