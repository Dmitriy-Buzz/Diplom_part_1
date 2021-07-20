import requests
import json
from tqdm import tqdm
from Yadisk import YaDisk

with open("token_yadisk.txt", encoding="utf-8") as file_tya:
    token_ya = file_tya.read().strip()

class Vkapi:
    def __init__(self, token, user_id, count=5, offset=0):
        self.token = token
        self.user_id = user_id
        self.count = count
        self.offset = offset

    def infor_user(self):
        URL = "https://api.vk.com/method/users.get"
        params = {
            'user_ids': '{}'.format(self.user_id),
            'access_token': '{}'.format(self.token),
            'v': '5.131'
        }
        res = requests.get(URL, params=params)
        user = (res.json())
        return user['response'][0]['first_name'] + ' ' + user['response'][0]['last_name']

    def info_users(self):
        URL = "https://api.vk.com/method/users.get"
        params = {
            'user_ids': '{}'.format(self.user_id),
            'fields': 'photo_id',
            'access_token': '{}'.format(self.token),
            'v': '5.131'
        }
        res = requests.get(URL, params=params)
        photo_id = (res.json()['response'][0]['photo_id'])
        num_id = photo_id.split('_')
        return num_id[0]

    def info_photos(self):
        user_id = self.info_users()
        URL = "https://api.vk.com/method/photos.get"
        params = {
            'owner_id': '{}'.format(user_id),
            'album_id': 'profile',
            'extended': '1',
            'photos_sizes': '1',
            'count':  self.count,
            'offset':  self.offset,
            'access_token': '{}'.format(self.token),
            'v': '5.131'
        }
        res = requests.get(URL, params=params)
        return res.json()

    def count_photos(self):
        data = self.info_photos()
        count_photo = data['response']['count']
        return count_photo

    def get_file_name(self):
        likes_l = []
        date_l = []
        base = self.info_photos()
        for files in base['response']['items']:
            likes_l.append(str(files['likes']['count']))
            date_l.append(str(files['date']))
        id_name = [i for i, x in enumerate(likes_l) if x in filter(lambda x: likes_l.count(x) > 1, set(likes_l))]
        for i in id_name:
            k = likes_l.pop(i)
            new_name = k + "_" + date_l[i]
            likes_l.insert(i, new_name)
        return likes_l

    def get_sizes(self):
        sizes_l = []
        base = self.info_photos()
        for files in base['response']['items']:
            sizes_l.append(files['sizes'][-1]['type'])
        return sizes_l

    def get_url(self):
        file_url = []
        base = self.info_photos()
        for files in base['response']['items']:
            file_url.append(files['sizes'][-1]['url'])
        return file_url

    def download_photos(self):
        photos_list = []
        all_name = self.get_file_name()
        all_size = self.get_sizes()
        all = dict(zip(all_name, all_size))
        file_name = []
        for key, value in all.items():
            file_name.append(key + '{}'.format('.jpg'))
            file_name_2 = key + '{}'.format('.jpg')
            photos_dict = {'File name': file_name_2, 'sizes': value}
            photos_list.append(photos_dict)
            with open('List_photos.json', 'w') as f:
                json.dump(photos_list, f)
        return file_name

    def upload_photos_ya(self):
        key_name = self.download_photos()
        url = self.get_url()
        all = dict(zip(key_name, url))
        for key, value in tqdm(all.items(), ascii=True, desc='Загрузка файлов на Yandex.disk'):
            get_url = requests.get(value)
            upload_ya = YaDisk(token=token_ya)
            upload_ya.upload_file_to_disk('Photos/{}'.format(key), get_url.content)