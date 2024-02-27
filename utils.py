import json


def get_cloud_service():
    """
    Запрашивает у пользователя выбор облачного хранилища.

    :return: Выбранное облачное хранилище (yandex, google) или пустая строка для резервного копирования в оба хранилища.
    """
    while True:
        cloud_service = input(
            "Выберите облачное хранилище (yandex, google) или нажмите Enter для резервного копирования в оба хранилища: ").strip().lower()
        if cloud_service in ["yandex", "google", ""]:
            return cloud_service
        else:
            print("Неверный ввод. Пожалуйста, выберите 'yandex', 'google' или оставьте поле пустым.")


def get_photo_count():
    """
    Запрашивает у пользователя количество фотографий для резервного копирования.

    :return: Количество фотографий для резервного копирования.
    """
    while True:
        try:
            count = int(input("Введите количество фотографий для резервного копирования: "))
            if count < 1:
                print("Количество фотографий должно быть больше 0.")
            else:
                return count
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")


def create_json_file(data: list, file_path: str):
    """
    Создает файл JSON и записывает в него переданные данные.

    :param data: Данные для записи в файл.
    :param file_path: Путь к файлу JSON.
    """
    with open(file_path, "w") as file:
        json.dump(data, file)
