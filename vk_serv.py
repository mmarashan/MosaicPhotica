import vk

session = vk.Session(access_token="ac")
vk_api = vk.API(session)
if __name__ == "__main__":
    friends = vk_api.friends.get(user_id="10230898", v=5.95)
    users = vk_api.users.get(user_ids=friends['items'], v=5.95, fields="photo_50")
    photos = [friend["photo_50"] for friend in users]
    print(photos)
