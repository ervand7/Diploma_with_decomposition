import hashlib  # для md5
from itertools import islice  # быстро разбить словарь на несколько словарей
from os.path import splitext, basename
from urllib.parse import urlencode  # это поможет в получении токена ОК
# следующие 2 модуля нужны чтобы получить расширение у url
from urllib.parse import urlparse
import requests
from Directory_OK.initial_user_inputs import for_ok_input

# __________________________________________________________________
# OK REST methods documentation https://apiok.ru/dev/methods/rest/
# data demanded from OK
BASE_URL = 'https://api.ok.ru/fb.do'  # take already generate from https://apiok.ru/dev/methods/rest/
# put here your 'Application public key' from email, which you got in response of your request in OK support
APPLICATION_KEY = ''
# put here your 'Application_secret_key' from email, which you got in response of your request in OK support
APPLICATION_SECRET_KEY = ''
FID = for_ok_input[0]
FORMAT = 'json'
METHOD = 'photos.getPhotos'
METHOD_2 = 'url.getInfo'  # to get id from nickname
# the service will independently generate a token in each section about the method. Take the token from there
ACCESS_TOKEN = ''
# ATTENTION! not to be confused this parameter with APPLICATION_SECRET_KEY!
SECRET_KEY = ''
SIG = ''
COUNT = for_ok_input[1]


# __________________________________________________________________

class OK:
    def __init__(self, access_token=ACCESS_TOKEN,
                 fid=FID, count=COUNT, method=METHOD, sig=SIG, secret_key=SECRET_KEY, format=FORMAT,
                 application_secret_key=APPLICATION_SECRET_KEY, application_key=APPLICATION_KEY, base_url=BASE_URL):
        self.access_token = access_token
        self.count = count
        self.fid = fid
        self.method = method
        self.sig = sig
        self.secret_key = secret_key
        self.format = format
        self.application_secret_key = application_secret_key
        self.application_key = application_key
        self.base_url = base_url

    # _________________________________________________________________________

    def get_secret_key(self):
        access_t_plus_apl_key = self.access_token + self.application_secret_key
        access_t_plus_apl_key_encode = access_t_plus_apl_key.encode()  # use 'from sys import getdefaultencoding'
        hash_access_t_plus_apl_key_encode = hashlib.md5(access_t_plus_apl_key_encode)
        self.secret_key = hash_access_t_plus_apl_key_encode.hexdigest().lower()
        return self.secret_key

    # _________________________________________________________________________

    def get_user_id_from_nickname(self):
        def get_sig_in_frames_nickname():
            sorted_params = (sorted(params_in_frames_nickname.items(), key=lambda x: x[0]))
            sort_par_k_equally_v = [(i[0] + '=' + str(i[1])) for i in sorted_params]
            glued_indexes = sort_par_k_equally_v[0] + sort_par_k_equally_v[1] + sort_par_k_equally_v[2] + \
                            sort_par_k_equally_v[
                                3] + sort_par_k_equally_v[4]
            glued_i_plus_secret_k = glued_indexes + self.get_secret_key()
            self.sig = hashlib.md5(glued_i_plus_secret_k.encode()).hexdigest().lower()
            return self.sig

        params_in_frames_nickname = {
            'application_key': APPLICATION_KEY,
            'format': FORMAT,
            'method': METHOD_2,
            'count': self.count,
            'url': f'https://ok.ru/{str(for_ok_input[0])}'
        }

        params_in_frames_nickname.update({'sig': get_sig_in_frames_nickname(), 'access_token': self.access_token})
        url_for_request_in_frames_nickname = ('?'.join([BASE_URL, urlencode(params_in_frames_nickname)]))
        response_in_frames_nickname = requests.get(url_for_request_in_frames_nickname)
        res_in_frames_nickname = response_in_frames_nickname.json()['objectId']
        return res_in_frames_nickname

    # _________________________________________________________________________

    def get_id_from_id(self):
        return self.fid

    # _________________________________________________________________________

    def get_lst_of_small_dicts(self):
        def get_sig_in_frames_available_id():
            sorted_params = (sorted(params.items(), key=lambda x: x[0]))
            sort_par_k_equally_v = [(i[0] + '=' + str(i[1])) for i in sorted_params]
            glued_indexes = sort_par_k_equally_v[0] + sort_par_k_equally_v[1] + sort_par_k_equally_v[2] + \
                            sort_par_k_equally_v[3] + sort_par_k_equally_v[4]
            glued_i_plus_secret_k = glued_indexes + self.get_secret_key()
            self.sig = hashlib.md5(glued_i_plus_secret_k.encode()).hexdigest().lower()
            return self.sig

        #  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
        if for_ok_input[0].isdigit():
            params = {
                'application_key': APPLICATION_KEY,
                'fid': self.get_id_from_id(),
                'format': FORMAT,
                'method': METHOD,
                'count': self.count
            }
        else:
            params = {
                'application_key': APPLICATION_KEY,
                'fid': self.get_user_id_from_nickname(),
                'format': FORMAT,
                'method': METHOD,
                'count': self.count
            }
        params.update({'sig': get_sig_in_frames_available_id(), 'access_token': self.access_token})
        url_for_request = ('?'.join([BASE_URL, urlencode(params)]))
        response = requests.get(url_for_request)
        res = response.json()['photos']

        #  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

        # _________________________________________________________________________

        def select_size_and_give_name():
            lst_comments_count_link_id = []
            for i in res:
                if 'pic640x480' in i:
                    a = (i['comments_count'], i['pic640x480'], i['id'])
                    lst_comments_count_link_id.append(list(a))
                elif 'pic128x128' in i:
                    a = (i['comments_count'], i['pic128x128'], i['id'])
                    lst_comments_count_link_id.append(list(a))
                elif 'pic50x50' in i:
                    a = (i['comments_count'], i['pic50x50'], i['id'])
                    lst_comments_count_link_id.append(list(a))
            # _______________________________________________

            for i in lst_comments_count_link_id:
                picture_page = i[1]
                disassembled = urlparse(picture_page)
                filename, file_ext = splitext(basename(disassembled.path))
                if file_ext == '':
                    i[0] = '_name-' + str(i[0]) + '||file_ext_is_not_defined'
                else:
                    i[0] = str(i[0]) + '_ext_' + file_ext
            # _______________________________________________

            update_lst_comments_count_link_id = []
            for i in lst_comments_count_link_id:
                if i[0] in [d[0] for d in update_lst_comments_count_link_id]:
                    i[0] = 'photo_id_' + str(i[2]) + i[0]
                update_lst_comments_count_link_id.append(i[0:2])
            # _______________________________________________

            single_dct_name_link = {}
            for i in update_lst_comments_count_link_id:
                single_dct_name_link[i[0]] = i[1]
            return single_dct_name_link
            # _______________________________________________

        def splitting_big_dct_into_many_small_dcts(data, size=0):
            it = iter(data)
            for i in range(0, len(data), size):
                yield {k: data[k] for k in islice(it, size)}

        lst_of_small_dicts = []
        for item in splitting_big_dct_into_many_small_dcts({i: a for i, a in select_size_and_give_name().items()}, 1):
            lst_of_small_dicts.append(item)
            # _______________________________________________
            # final arrangement of elements
        for i in lst_of_small_dicts:
            for name_with_ext in list(i):
                i['file_name'] = name_with_ext
            for key in list(i):
                if '_ext_' in key:
                    i['file_link'] = i[key]
                if '_ext_' in key:
                    i.pop(key)

        return lst_of_small_dicts  # the most important element in program
