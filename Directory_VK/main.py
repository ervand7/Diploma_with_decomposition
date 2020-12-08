import requests
from tqdm import tqdm  # прогресс-бар
from Directory_VK.initial_user_inputs import for_vk_input_items, folder_input, json_input
from Directory_VK.description_of_class_vk import VKUser
from Directory_VK.tokens_and_other_service_info import YANDEX_TOKEN
from Directory_VK.creating_yandex_folder import YandexFolderCreating
from Directory_VK.creating_json_file import creating_json_file


# Процесс записи данных в Яндекс.Диск из переменной lst_of_small_dicts, которая является
# результатом от experimental.get_list_of_small_dicts()
class YaUpPhotoFromVk:
    def __init__(self, token=YANDEX_TOKEN):
        self.token = token
        for i in tqdm(exemplar_from_class_vk.get_list_of_small_dicts()):
            requests.post(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                params={"url": i["file_link"],
                        "path": f'{folder_input}/{i["file_name"]}'},
                headers={"Authorization": f"OAuth {YANDEX_TOKEN}", }
            )


print('\nПожалуйста, подождите. Идет загрузка файлов на Яндекс.Диск.')

# ``````````````````````````````````````````````````````````````````````

if __name__ == '__main__':
    exemplar_from_class_vk = VKUser()
    yandex_disk_folder = YandexFolderCreating()
    creating_json_file(exemplar_from_class_vk)
    yandex_uploader = YaUpPhotoFromVk()

    print(
        f'Фотографии максимального размера ({for_vk_input_items[1]} шт.) '
        f'успешно загружены на Яндекс.Диск в папку под названием "{folder_input}".')

# use for example: 280572200 12
# use or example: pikalovpavel 12
