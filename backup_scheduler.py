from datetime import datetime, timedelta
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from db_types import DATABASE_TYPE_MYSQL
from backup_handlers import MySQLBackupHandler
from google_drive_handler import GoogleDriveHandler


class BackupScheduler(object):

    def __init__(self, logger):
        self._database_type = os.environ['DATABASE_TYPE']
        self._schedule = os.environ['SCHEDULE']
        self._days_to_keep_backups = int(os.environ['DAYS_TO_KEEP_BACKUPS'])
        self._logger = logger
        self._scheduler = BlockingScheduler()
        self._scheduler.add_job(self.handle_backups,
                                CronTrigger.from_crontab(self._schedule))

        self._google_drive_backup_enabled = os.environ.get(
            'GOOGLE_DRIVE_BACKUP_ENABLED', 'true') == 'true'

    def handle_backups(self):
        if self._database_type == DATABASE_TYPE_MYSQL:
            handler = MySQLBackupHandler(logger=self._logger)
            backup_filename = handler.backup()
            limit_dt = datetime.utcnow() - timedelta(
                days=self._days_to_keep_backups)
            removed_filenames = handler.clean_backups_before_time(limit_dt)

            if self._google_drive_backup_enabled:
                self._handle_google_drive_backups(backup_filename,
                                                  removed_filenames)

    def _handle_google_drive_backups(self, backup_filename, removed_filenames):
        gdrive_handler = GoogleDriveHandler()
        gdrive_handler.upload_file(backup_filename)
        gdrive_handler.remove_files(removed_filenames)

    def run(self):
        self._scheduler.start()
