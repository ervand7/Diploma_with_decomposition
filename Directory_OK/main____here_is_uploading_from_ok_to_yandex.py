# The task https://github.com/netology-code/py-diplom-basic
# The same program for VK https://github.com/ervand7/Diploma/blob/master/Diploma.py
import requests
from tqdm import tqdm
from Directory_OK.description_of_class_ok import OK
from Directory_OK.creating_json_file import creating_json_file
from Directory_OK.initial_user_inputs import for_ok_input, folder_input
from Directory_OK.creating_yandex_folder import YandexFolderCreating, YANDEX_TOKEN


class YaUpPhotoFromOk:
    def __init__(self, token=YANDEX_TOKEN):
        self.token = token
        for i in tqdm(OK.get_lst_of_small_dicts(exemplar_from_class_ok)):
            requests.post(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                params={"url": i["file_link"],
                        "path": f'{folder_input}/{i["file_name"]}'},
                headers={"Authorization": f"OAuth {YANDEX_TOKEN}", }
            )


print('\nПожалуйста, подождите. Идет загрузка файлов на Яндекс.Диск.')

# ``````````````````````````````````````````````````````````````````````

if __name__ == '__main__':
    exemplar_from_class_ok = OK()
    yandex_disk_folder = YandexFolderCreating()
    creating_json_file(exemplar_from_class_ok)
    yandex_uploader = YaUpPhotoFromOk()

    print(
        f'Фотографии максимального размера ({for_ok_input[1]} шт.) '
        f'успешно загружены на Яндекс.Диск в папку под названием "{folder_input}".')

# use for id: 576339763099
# use for nickname: peftiev
