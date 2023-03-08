from datetime import datetime
import os

from process import run_command

TIMESTAMP_FORMAT = '%Y-%m-%dT%H-%M-%S'


class MySQLBackupHandler(object):

    def __init__(self, logger=None):
        self._database_host = os.environ['MYSQL_HOST']
        self._database_port = os.environ['MYSQL_PORT']
        self._database_user = os.environ['MYSQL_USER']
        self._database_password = os.environ['MYSQL_PASSWORD']
        self._database_name = os.environ['MYSQL_DATABASE_NAME']
        self._output_folder = os.environ['OUTPUT_FOLDER']
        self._logger = logger

    def backup(self):
        timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
        target_filename = f'{self._database_name}-{timestamp}.sql'
        output_path = os.path.join(self._output_folder, target_filename)
        command = f"""
            mysqldump \
                --host={self._database_host} \
                --port={self._database_port} \
                --user={self._database_user} \
                --password='{self._database_password}' {self._database_name} > {output_path}
            """
        run_command(command)

        return target_filename

    def clean_backups_before_time(self, limit_dt):
        removed_backups = []
        for filename in os.listdir(self._output_folder):
            if filename.startswith(
                    f"{self._database_name}-") and filename.endswith(".sql"):
                timestamp = filename.lstrip(f"{self._database_name}-").rstrip(
                    ".sql")
                try:
                    file_dt = datetime.strptime(timestamp, TIMESTAMP_FORMAT)

                    if file_dt < limit_dt:
                        self._logger.info(f"Removing old backup: {filename}")
                        file_path = os.path.join(self._output_folder, filename)
                        os.remove(file_path)
                        removed_backups.append(filename)
                except ValueError:
                    self._logger.warn(
                        f"File f{filename} not created by backup handler")

        return removed_backups
