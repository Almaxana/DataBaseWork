FROM python:latest
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
WORKDIR /py_root
CMD ["python", "-u", "start_insert_migrations.py"]
CMD ["python", "-u", "backups/backupCreation.py"]
