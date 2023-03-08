from datetime import datetime
import os

from process import run_command


class MySQLBackupHandler(object):

    def __init__(self):
        self._database_host = os.environ['MYSQL_HOST']
        self._database_port = os.environ['MYSQL_PORT']
        self._database_user = os.environ['MYSQL_USER']
        self._database_password = os.environ['MYSQL_PASSWORD']
        self._database_name = os.environ['MYSQL_DATABASE_NAME']
        self._output_folder = os.environ['OUTPUT_FOLDER']

    def backup(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
        target_filename = f'{self._database_name}-{timestamp}.sql'
        output_path = os.path.join(self._output_folder, target_filename)
        command = f"""
            mysql \
                --host={self._database_host} \
                --port={self._database_port} \
                --user={self._database_user} \
                --password='{self._database_password}' > {output_path}
            """
        run_command(command)
