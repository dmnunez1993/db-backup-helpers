import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GoogleDriveHandler(object):

    def __init__(self):
        self._google_drive_secrets_file = os.environ[
            'GOOGLE_DRIVE_SECRETS_FILE']
        self._google_drive_credentials_file = os.environ[
            'GOOGLE_DRIVE_CREDENTIALS_FILE']
        self._google_drive_folder_id = os.environ[
            'GOOGLE_DRIVE_BACKUP_FOLDER_ID']
        self._backup_folder = os.environ['BACKUP_FOLDER']
        GoogleAuth.DEFAULT_SETTINGS[
            'client_config_file'] = self._google_drive_secrets_file

        self._gauth = GoogleAuth()

        self._gauth.LoadCredentialsFile(self._google_drive_credentials_file)

        if self._gauth.credentials is None:
            self._gauth.LocalWebserverAuth()
        elif self._gauth.access_token_expired:
            self._gauth.Refresh()
        else:
            self._gauth.Authorize()

        self._gauth.SaveCredentialsFile(self._google_drive_credentials_file)

        self._drive = GoogleDrive(self._gauth)

    def upload_file(self, filename):
        file_path = os.path.join(self._backup_folder, filename)
        gdrive_file = self._drive.CreateFile({
            'title': filename,
            'parents': [{
                'id': self._backup_folder
            }]
        })
        gdrive_file.SetContentFile(file_path)
        gdrive_file.Upload()
