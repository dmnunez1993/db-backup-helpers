FROM python:3.9.6-alpine

RUN apk update && apk add build-base gcc python3-dev musl-dev libffi-dev freetype-dev mysql-client zip

RUN mkdir /db_backups

COPY ./requirements.txt /db_backups/requirements.txt

WORKDIR /db_backups

RUN pip install pip==21.2.4
RUN pip install -r requirements.txt

COPY ./. /db_backups/

CMD ["python3", "run_backup_scheduler.py"]
