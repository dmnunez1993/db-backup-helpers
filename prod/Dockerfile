FROM python:3.9.6-alpine

RUN apk update && apk add build-base gcc python3-dev musl-dev libffi-dev freetype-dev mysql-client

RUN mkdir /db_backups

COPY ./requirements.txt /db_backups/requirements.txt

WORKDIR /db_backups

RUN pip install pip==21.2.4
RUN pip install -r requirements.txt

COPY ./backup_handlers.py /db_backups/backup_handlers.py
COPY ./backup_scheduler.py /db_backups/backup_scheduler.py
COPY ./db_types.py /db_backups/db_types.py
COPY ./google_drive_handler.py /db_backups/google_drive_handler.py
COPY ./process.py /db_backups/process.py
COPY ./run_backup_scheduler.py /db_backups/run_backup_scheduler.py

CMD ["python3", "run_backup_scheduler.py"]
