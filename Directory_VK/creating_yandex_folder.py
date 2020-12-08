# Процесс создания папки на Яндекс.Диске
import requests
from Directory_VK.tokens_and_other_service_info import YANDEX_TOKEN
from Directory_VK.initial_user_inputs import folder_input


class YandexFolderCreating:
    def __init__(self, folder_name=folder_input, token=YANDEX_TOKEN):
        self.token = token
        self.folder_name = folder_name

        requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            params={"path": self.folder_name},
            headers={"Authorization": f"OAuth {YANDEX_TOKEN}"}
        )
        print(f'\nThe folder with name "{folder_name}" is successfully created on Yandex.Disk.')
