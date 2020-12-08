from urllib.parse import urlparse
from urllib.parse import urljoin
from os.path import splitext, basename
import requests
from itertools import islice  # быстро разбить словарь на несколько словарей
from Directory_VK.initial_user_inputs import wall_or_profile_album, for_vk_input_items
from Directory_VK.tokens_and_other_service_info import API_BASE_URL, VK_TOKEN, V


# Работаем с ВК и в итоге получаем переменную lst_of_small_dicts, в которой у нас будут все
# названия, требуемые в задании, ссылки, размеры и тд. Потом, уже на основе этой переменной
# будет создан json-файл и, опять же, на основе итерации по этой переменной, будет загрузка в Яндекс.Диск
class VKUser:
    def __init__(self, album=wall_or_profile_album, token=VK_TOKEN, version=V,
                 id=for_vk_input_items[0], count=for_vk_input_items[1]):
        self.token = token
        self.version = version
        self.count = count
        self.owner_id = id
        self.album = album

    def get_user_id_if_nickname(self):
        url_for_demand = urljoin(API_BASE_URL, 'users.get')
        response = requests.get(url_for_demand, params={
            'access_token': self.token,
            'v': self.version,
            'user_ids': self.owner_id,

        })
        found_id = response.json()['response'][0]['id']
        return found_id

    def get_list_of_small_dicts(self):
        data_for_vk = urljoin(API_BASE_URL, 'photos.get')
        # print(data_for_vk)
        response = requests.get(data_for_vk, params={
            'access_token': self.token,
            'v': self.version,
            'owner_id': self.get_user_id_if_nickname(),
            'album_id': self.album,
            'extended': 1,
            'count': self.count
        })

        # __________________________________________________________________
        # Получаем фотки в виде списка, каждое значение из которого: лайк - ссылка - дата
        # В этом блоке выполняем условие задания - загружать только самые большие по размеру фото
        def big_func_select_size_extension_naming():
            def select_size():
                lst_like_link_date = []
                res = response.json()['response']['items']
                # pprint(res)
                for i in res:
                    if 'photo_2560' in i:
                        a = (i['likes']['count'], i['photo_2560'], i['date'])
                        lst_like_link_date.append(list(a))
                    elif 'photo_1280' in i:
                        a = (i['likes']['count'], i['photo_1280'], i['date'])
                        lst_like_link_date.append(list(a))
                    elif 'photo_807' in i:
                        a = (i['likes']['count'], i['photo_807'], i['date'])
                        lst_like_link_date.append(list(a))
                    elif 'photo_604' in i:
                        a = (i['likes']['count'], i['photo_604'], i['date'])
                        lst_like_link_date.append(list(a))
                    elif 'photo_130' in i:
                        a = (i['likes']['count'], i['photo_130'], i['date'])
                        lst_like_link_date.append(list(a))
                    elif 'photo_75' in i:
                        a = (i['likes']['count'], i['photo_75'], i['date'])
                        lst_like_link_date.append(list(a))
                return lst_like_link_date

            # __________________________________________________________________
            # Получаем расширение и прилепляем его к str_показателю кол-ва лайков
            # Для этого используем from os.path import splitext, basename и from urllib.parse import urlparse
            def get_extension():
                list_like_link_date = select_size()
                for like_link_date in list_like_link_date:
                    link_ = like_link_date[1]
                    disassembled = urlparse(link_)
                    filename, file_ext = splitext(basename(disassembled.path))  # теперь у нас отдельно есть file_ext
                    like_link_date[0] = str(like_link_date[0]) + '_ext_' + file_ext
                return list_like_link_date

            # __________________________________________________________________
            # Если название, оно же и str_показатель кол-ва лайков, уже есть в update_lst_like_link_date,
            # то мы к его названию еще прилепляем и дату загузки (такое условие у задания).
            # Ну и, соответственно, в update_lst_like_link_date мы уже не берем последний элемент
            # из lst_like_link_date, то есть date, так как сейчас
            # мы с ним поработали, от него взяли все нужное, и больше он нам не нужен.
            def get_naming():
                update_lst_like_link_date = []
                for like_link_date in get_extension():
                    if like_link_date[0] in [elem[0] for elem in update_lst_like_link_date]:
                        like_link_date[0] = 'date_' + str(like_link_date[2]) + '|name_' + like_link_date[0]
                    update_lst_like_link_date.append(like_link_date[0:2])
                return update_lst_like_link_date

            # __________________________________________________________________
            # Теперь трансформируем update_lst_like_link_date в словарь single_dct_name_link,
            # в котором ключ - это название файла, а значение - ссылка.
            # Этот словарь нужен, чтобы потом его разбить на словарь словарей и далее уже
            # значения подгонять под нужные нам параметры.
            def get_single_dct_name_link():
                single_dct_name_link = {}
                for update_lst_like_link_date in get_naming():
                    single_dct_name_link[update_lst_like_link_date[0]] = update_lst_like_link_date[1]
                return single_dct_name_link

            return get_single_dct_name_link()

        # __________________________________________________________________
        # Теперь разбиваем словарь на мелкие словари (имя: ссылка) и оборачиваем их в список
        def splitting_big_dct_into_many_small_dicts(initial_dict, start_from_first_element=1):
            iter_initial_dict = iter(initial_dict)
            for unit in range(len(initial_dict)):
                yield {key_: initial_dict[key_] for key_ in islice(iter_initial_dict, start_from_first_element)}

        n = splitting_big_dct_into_many_small_dicts

        lst_of_small_dicts = []
        for item in n(big_func_select_size_extension_naming()):
            lst_of_small_dicts.append(item)

        # __________________________________________________________________
        # Лепим из этого lst_of_small_dicts, элементы которого
        # сейчас представляют собой название: ссылка, нужные нам параметры.
        # Тут мы как бы сдвигаем ключ в значение, а на месте ключа прописываем 'file_name'
        def last_step_for_get_lst_of_small_dicts():
            for _item in lst_of_small_dicts:
                for name_with_ext in list(
                        _item):  # Оборач i в list мы избег. ош.: dictionary changed size during iteration
                    _item['file_name'] = name_with_ext
                # Берем наш изначальный элемент i (словарь, которых много в списке lst_of_small_dicts)
                # и создаем внутри этого словаря новый ключ 'file_link', и даем ему значение
                # изначального ключа, то есть ссылку.
                for key in list(_item):  # Оборачивая i в list мы избег. ош.: dictionary changed size during iteration
                    if '_ext_' in key:
                        _item['file_link'] = _item[key]
                    # Все сделали. Избавляемся теперь от ненужного изначального элемента название - ссылка.
                    if '_ext_' in key:
                        _item.pop(key)  # удаляем ключ, а вместе с ним и значение
            return lst_of_small_dicts

        return last_step_for_get_lst_of_small_dicts()