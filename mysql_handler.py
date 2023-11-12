from datetime import datetime
from logging import Logger
import os

from process import run_command

TIMESTAMP_FORMAT = '%Y-%m-%dT%H-%M-%S'


class MySQLBackupHandler(object):

    def __init__(self, logger: Logger):
        self._database_host = os.environ['MYSQL_HOST']
        self._database_port = os.environ['MYSQL_PORT']
        self._database_user = os.environ['MYSQL_USER']
        self._database_password = os.environ['MYSQL_PASSWORD']
        self._database_name = os.environ['MYSQL_DATABASE_NAME']
        self._backup_folder = os.environ['BACKUP_FOLDER']
        self._logger = logger

    def backup(self):
        timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
        target_filename_sql = f'{self._database_name}-{timestamp}.sql'
        target_filename_zip = f'{self._database_name}-{timestamp}.zip'
        output_path_sql = os.path.join(self._backup_folder, target_filename_sql)
        self._logger.info(
            f"Creating MySQL backup with name: {target_filename_sql}")
        command = f"""
            mysqldump \
                --host={self._database_host} \
                --port={self._database_port} \
                --user={self._database_user} \
                --password='{self._database_password}' {self._database_name} > {output_path_sql}
            """
        run_command(command)

        self._logger.info(f"Compressing backup to file {target_filename_zip}")

        command = f"cd {self._backup_folder} && zip -r {target_filename_zip} {target_filename_sql}"
        run_command(command)

        os.remove(output_path_sql)

        return target_filename_zip

    def clean_backups_before_time(self, limit_dt):
        removed_backups = []
        for filename in os.listdir(self._backup_folder):
            if filename.startswith(
                    f"{self._database_name}-") and filename.endswith(".sql"):
                timestamp = filename.lstrip(f"{self._database_name}-").rstrip(
                    ".sql")
                try:
                    file_dt = datetime.strptime(timestamp, TIMESTAMP_FORMAT)

                    if file_dt < limit_dt:
                        self._logger.info(f"Removing old backup: {filename}")
                        file_path = os.path.join(self._backup_folder, filename)
                        os.remove(file_path)
                        removed_backups.append(filename)
                except ValueError:
                    self._logger.warn(
                        f"File f{filename} not created by backup handler")

        return removed_backups
