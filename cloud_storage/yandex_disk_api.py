import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YandexDiskAPI:
    """
    Класс для взаимодействия с API Яндекс.Диска.
    """
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token=None):
        self.__access_token = token or input("Введите токен Яндекс.Диска: ")
        self.__headers = {
            'Authorization': f'OAuth {self.__access_token}',
            'Content-Type': 'application/json',
        }

    def _build_url(self, api_method):
        """
        Строит URL для API-запроса.

        :param api_method: Метод API.
        :return: Полный URL для запроса.
        """
        return f"{self.API_BASE_URL}/{api_method}"

    def put_create_folder(self, folder_name):
        """
        Создает папку на Яндекс.Диске.

        :param folder_name: Название папки.
        """
        params = {
            'path': folder_name,
        }

        response = requests.put(self.API_BASE_URL, headers=self.__headers, params=params)

        if response.status_code == 201:
            logger.info(f"Папка '{folder_name}' успешно создана.")
        elif response.status_code == 409:
            logger.info(f"Папка '{folder_name}' уже существует.")
        else:
            logger.error(f"Ошибка при создании папки '{folder_name}': {response.text}")

    def post_upload_photo(self, folder_name, photo_url, file_name):
        """
        Загружает фото на Яндекс.Диск.

        :param folder_name: Название папки.
        :param photo_url: URL фотографии.
        :param file_name: Имя файла.
        """
        params = {
            'path': f'/{folder_name}/{file_name}.jpg',
            'url': photo_url,
        }

        response = requests.post(self._build_url('upload'), headers=self.__headers, params=params)

        if response.status_code == 202:
            logger.info('Фото успешно загружено в папку')
        else:
            logger.error('Ошибка при загрузке фото: %d', response.status_code)

    def upload_photos_disk(self, folder_name, photos_info):
        """
        Загружает фотографии на Яндекс.Диск.

        :param folder_name: Название папки.
        :param photos_info: Информация о фотографиях.
        """
        self.put_create_folder(folder_name=folder_name)

        for photo_data in photos_info:
            self.post_upload_photo(folder_name=folder_name, photo_url=photo_data["link_photo"],
                                   file_name=photo_data["name"])
