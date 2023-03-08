#!/usr/bin/env python
from datetime import datetime
import os
import logging

from dotenv import load_dotenv

from db_types import DATABASE_TYPE_MYSQL
from backup_handlers import MySQLBackupHandler

if os.path.isfile(".env"):
    load_dotenv(os.path.join(".env"))

DATABASE_TYPE = os.environ['DATABASE_TYPE']

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

logger = logging.getLogger('db_backupgs_scheduler')
logger.setLevel(logging.DEBUG)


def main():
    if DATABASE_TYPE == DATABASE_TYPE_MYSQL:
        handler = MySQLBackupHandler(logger=logger)
        handler.backup()
        handler.clean_backups_before_time(datetime.now())


if __name__ == '__main__':
    main()
