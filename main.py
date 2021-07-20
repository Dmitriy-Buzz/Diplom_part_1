from VK import Vkapi

with open("token_vk.txt", encoding="utf-8") as file_tvk:
    token_vk = file_tvk.read().strip()

HELP = """
Добрый день, Вы находитесь в программе скачиваения фотографий профиля из Вконтакте, 
для начала работы, необходимо:
1. Создать в каталоге программы 2 файла формата txt;
1.1 Файл txt с токеном VK
1.1 Файл txt с токеном Yadisk
2. На Yandex.disk необходимо создать папку 'Photos/'
3. Ввести id пользователя, либо screen_name.
4. Нажать 'Enter', Вы увидите строку загрузки файлов.
5. После загрузки в каталоге программы появиться файл: 'List_photos' с называнием и размером фотографий

Список доступных команд:
help - справка по программе

id - ввести id, либо screen_name (числовой формат пример:№11547416, либо пример:*timatimusic*);

exit - команда, выход из программы
"""

def main():
    print('Программа скачивания фотографий из VK.com на Yandex.disk\n'
          'справка по программе: help\n')
    stop = False
    while not stop:
        command = input("Введите команду:\n")
        if command == "help":
            print(HELP)
        elif command == "id":
            user_id_input = input('Введите screen_name либо id пользователя:№\n')
            info_vk = Vkapi(token=token_vk, user_id=user_id_input)
            print(f'Пользователь {info_vk.infor_user()} id № {user_id_input} количество фотографий в профиле: {info_vk.count_photos()}')
            user_count_photos = input('Введите количество фотографий на скачивание:\n')
            down_vk = Vkapi(token=token_vk, user_id=user_id_input, count=int(user_count_photos))
            down_vk.upload_photos_ya()
        elif command == "exit":
            print("Спасибо за использование программы")
            stop = True
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()