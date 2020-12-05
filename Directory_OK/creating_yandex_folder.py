from Directory_OK.initial_user_inputs import folder_input
import requests

# __________________________________________________________________
# Put here your token from https://yandex.ru/dev/disk/poligon/
YANDEX_TOKEN = ''
# __________________________________________________________________


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
