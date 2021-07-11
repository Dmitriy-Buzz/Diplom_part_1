from VK import Vkapi

with open("token_vk.txt", encoding="utf-8") as file_tvk:
    token_vk = file_tvk.read().strip()

down_vk = Vkapi(token=token_vk)
down_vk.upload_photos_ya()