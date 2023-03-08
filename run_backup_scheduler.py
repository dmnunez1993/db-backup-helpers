#!/usr/bin/env python
import os

from dotenv import load_dotenv

from db_types import DATABASE_TYPE_MYSQL
from backup_handlers import MySQLBackupHandler

if os.path.isfile(".env"):
    load_dotenv(os.path.join(".env"))

DATABASE_TYPE = os.environ['DATABASE_TYPE']


def main():
    if DATABASE_TYPE == DATABASE_TYPE_MYSQL:
        print("here")
        handler = MySQLBackupHandler()
        handler.backup()


if __name__ == '__main__':
    main()
