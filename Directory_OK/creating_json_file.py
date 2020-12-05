import os
import json
from Directory_OK.initial_user_inputs import json_input


def creating_json_file(exemplar_from_class_ok):
    json_file = dict()
    json_file['info'] = exemplar_from_class_ok.get_lst_of_small_dicts()

    file_path = os.path.join(os.getcwd(), f'{json_input}.json')
    with open(file_path, 'w+') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)

    print(
        f'\nДанные в требуемом заданием формате успешно записаны в \n'
        f'только что созданный вами json-файл под названием "{json_input}.json".'
        f'\nЭтот json-файл вы можете найти в памяти своего ПК.')
