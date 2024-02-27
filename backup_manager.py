import logging
import time

from cloud_storage.google_drive_api import GoogleDriveAPI
from cloud_storage.utils.utils import preparing_upload_photos
from cloud_storage.yandex_disk_api import YandexDiskAPI
from utils import create_json_file
from vk.vk_api import VKAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudService:
    """Класс для представления облачных сервисов."""
    YANDEX = 'yandex'
    GOOGLE = 'google'


class BackupManager:
    """Класс для управления резервным копированием фотографий."""

    def __init__(self, count: int = 5):
        self.__count = count

    def backup_photos(self, cloud_service: str):
        """
        Выполняет резервное копирование фотографий в указанное облачное хранилище.

        :param cloud_service: Наименование облачного сервиса.
                              Допустимые значения: 'yandex', 'google' или '' (пустая строка).
        :raises ValueError: Если указан неверный облачный сервис.
        """
        if cloud_service not in [CloudService.YANDEX, CloudService.GOOGLE, '']:
            raise ValueError("Указан неверный облачный сервис.")

        vk_api = VKAPI()

        folder_name = input("Введите название папки: ")
        user_photos_info = vk_api.get_user_photos_info(count=self.__count)

        new_photos_info = preparing_upload_photos(photos_info=user_photos_info)

        time.sleep(1)

        if cloud_service in [CloudService.YANDEX, '']:
            self._backup_to_yandex(folder_name=folder_name, user_photos_info=new_photos_info)
            logger.info("Фотографии успешно загружены в Яндекс.Диск")

        if cloud_service in [CloudService.GOOGLE, '']:
            self._backup_to_google(folder_name=folder_name, user_photos_info=new_photos_info)
            logger.info("Фотографии успешно загружены в Google Диск")

        create_json_file(new_photos_info, "backup_photos.json")
        logger.info("Создан файл JSON с информацией о резервных копиях")

    def _backup_to_yandex(self, folder_name, user_photos_info):
        """
        Выполняет резервное копирование фотографий в Яндекс.Диск.

        :param folder_name: Название папки в Яндекс.Диске.
        :param user_photos_info: Информация о фотографиях для резервного копирования.
        """
        yandex_disk_api = YandexDiskAPI()
        yandex_disk_api.upload_photos_disk(folder_name, user_photos_info)

    def _backup_to_google(self, folder_name, user_photos_info):
        """
        Выполняет резервное копирование фотографий в Google Диск.

        :param folder_name: Название папки в Google Диске.
        :param user_photos_info: Информация о фотографиях для резервного копирования.
        """
        google_api = GoogleDriveAPI()
        google_api.upload_photos_disk(folder_name=folder_name, photos_info=user_photos_info)
