import io
import os
import logging
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleDriveAPI:
    """
    Класс для взаимодействия с API Google Drive.
    """

    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('/', '\\')
        self.__client_secrets_path = root_path + "/config/client_secrets.json"
        self.__credentials_path = root_path + "/config/credentials.json"

        self.__drive = self.__authenticate_google_drive()

    def __authenticate_google_drive(self):
        """
        Аутентификация в Google Drive.
        """
        gauth = GoogleAuth()
        gauth.settings['client_config_file'] = self.__client_secrets_path

        if os.path.exists(self.__credentials_path):
            gauth.LoadCredentialsFile(self.__credentials_path)
        else:
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(self.__credentials_path)

        return GoogleDrive(gauth)

    def put_create_folder(self, folder_name):
        """
        Создает папку на Google Drive.

        :param folder_name: Название папки.
        :return: Название и идентификатор созданной папки.
        """
        folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = self.__drive.CreateFile(folder_metadata)
        folder.Upload()

        logger.info('Папка создана: title: %s, id: %s', folder['title'], folder['id'])

        return folder['title'], folder['id']

    def post_upload_photo(self, folder_id, photo_url, file_name):
        """
        Загружает фотографию на Google Drive.

        :param folder_id: Идентификатор папки.
        :param photo_url: URL фотографии.
        :param file_name: Имя файла.
        :return: Название и идентификатор загруженной фотографии.
        """
        file_metadata = {'title': file_name, 'parents': [{'id': folder_id}]}

        image_content = io.BytesIO(requests.get(photo_url).content)
        file = self.__drive.CreateFile(file_metadata)
        file.content = image_content
        file.Upload()

        logger.info('Фотография загружена: title: %s, id: %s', file['title'], file['id'])

        return file['title'], file['id']

    def upload_photos_disk(self, folder_name, photos_info):
        """
        Загружает фотографии на Google Drive.

        :param folder_name: Название папки.
        :param photos_info: Информация о фотографиях.
        """
        title, folder_id = self.put_create_folder(folder_name=folder_name)

        for photo_data in photos_info:
            self.post_upload_photo(
                folder_id=folder_id,
                photo_url=photo_data["link_photo"],
                file_name=photo_data["name"]
            )
