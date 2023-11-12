from datetime import datetime, timedelta
from logging import Logger
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from db_types import DATABASE_TYPE_MYSQL
from mysql_handler import MySQLBackupHandler
from google_drive_handler import GoogleDriveHandler


class BackupScheduler(object):

    def __init__(self, logger: Logger):
        self._database_type = os.environ['DATABASE_TYPE']
        self._schedule = os.environ['SCHEDULE']
        self._days_to_keep_backups = int(os.environ['DAYS_TO_KEEP_BACKUPS'])
        self._logger = logger
        self._scheduler = BlockingScheduler()
        self._scheduler.add_job(self.handle_backups,
                                CronTrigger.from_crontab(self._schedule))

        self._google_drive_backup_enabled = os.environ.get(
            'GOOGLE_DRIVE_BACKUP_ENABLED', 'true') == 'true'
        self._google_drive_handler = GoogleDriveHandler()

        if self._google_drive_backup_enabled:
            self._scheduler.add_job(self.refresh_google_credentials,
                                    CronTrigger.from_crontab("*/10 * * * *"))

        self._creating_backup = False

    def refresh_google_credentials(self):
        self._google_drive_handler.authorize()

    def handle_backups(self):
        if self._creating_backup:
            self._logger.info("Backup creation already in process! Skipping...")
            return

        self._creating_backup = True

        if self._database_type == DATABASE_TYPE_MYSQL:
            handler = MySQLBackupHandler(logger=self._logger)
            backup_filename = handler.backup()
            limit_dt = datetime.utcnow() - timedelta(
                days=self._days_to_keep_backups)
            removed_filenames = handler.clean_backups_before_time(limit_dt)

            if self._google_drive_backup_enabled:
                self._handle_google_drive_backups(backup_filename,
                                                  removed_filenames)

        self._creating_backup = False

    def _handle_google_drive_backups(self, backup_filename, removed_filenames):
        self._google_drive_handler.authorize()
        self._google_drive_handler.upload_file(backup_filename)
        self._google_drive_handler.remove_files(removed_filenames)

    def run(self):
        self._scheduler.start()
