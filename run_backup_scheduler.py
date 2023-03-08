#!/usr/bin/env python
import os
import logging

from dotenv import load_dotenv

from backup_scheduler import BackupScheduler

if os.path.isfile(".env"):
    load_dotenv(os.path.join(".env"))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

logger = logging.getLogger('db_backupgs_scheduler')
logger.setLevel(logging.DEBUG)


def main():
    scheduler = BackupScheduler(logger=logger)
    scheduler.run()


if __name__ == '__main__':
    main()
