from datetime import datetime
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from db_types import DATABASE_TYPE_MYSQL
from backup_handlers import MySQLBackupHandler


class BackupScheduler(object):

    def __init__(self, logger):
        self._database_type = os.environ['DATABASE_TYPE']
        self._schedule = os.environ['SCHEDULE']
        self._logger = logger
        self._scheduler = BlockingScheduler()
        self._scheduler.add_job(self.handle_backups,
                                CronTrigger.from_crontab(self._schedule))

    def handle_backups(self):
        if self._database_type == DATABASE_TYPE_MYSQL:
            handler = MySQLBackupHandler(logger=self._logger)
            handler.backup()
            handler.clean_backups_before_time(datetime.now())

    def run(self):
        self._scheduler.start()
