from backup_manager import BackupManager
from utils import *


def main():
    try:
        cloud_service = get_cloud_service()
        count = get_photo_count()

        backup_manager = BackupManager(count=count)
        backup_manager.backup_photos(cloud_service=cloud_service)
    except Exception as e:
        print("Произошла ошибка:", e)


if __name__ == "__main__":
    main()
