import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard
import random


import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor



def main():
    token = "vk1.a.ks1r-nPDKh57EgLcAdr3KSf50HSWQc48niM3rqsondwyswzfdbCATJV0Y5s4rooHfMBzWIen6fWVkveiexkTC6DsLLGWV_fpJuwpjYPHV14-SAyTNloslO0K82FqDWEQL_lsgjE5zDjV8Ogxj0e9ofYgwMQyBitc6zEIIKRqMFv4Ui54cOSWcT5UnV3e9cMOqy1G9PWkOnLVscYEhtHRwA"
    vk_sesion = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_sesion, "224556618")
    setting = dict(one_time=False, inline=True)
    keyboard = VkKeyboard(**setting)
    keyboard.add_callback_button("Войти", VkKeyboardColor.PRIMARY,payload={"type": "show_snackbar", "text":"Это исчезающее сообщение"})

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_sesion.get_api()
            user_message = event.obj.message["text"]
            if user_message == "Начать":
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Начинаю работу",
                                 random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())


                


            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Спасибо, что написали нам. Мы обязательно ответим",
                             random_id=random.randint(0, 1000000000))




"""token = "vk1.a.ks1r-nPDKh57EgLcAdr3KSf50HSWQc48niM3rqsondwyswzfdbCATJV0Y5s4rooHfMBzWIen6fWVkveiexkTC6DsLLGWV_fpJuwpjYPHV14-SAyTNloslO0K82FqDWEQL_lsgjE5zDjV8Ogxj0e9ofYgwMQyBitc6zEIIKRqMFv4Ui54cOSWcT5UnV3e9cMOqy1G9PWkOnLVscYEhtHRwA"
avtorize = vk_api.VkApi(token=token)



def write_message(sender, message, keyboard):
    avtorize.method("messages.send", )

def main():
    longpoll = VkLongPoll(avtorize)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Сообщение от:", event.user_id)
            print("Текст: ", event.text)
            sender = event.user_id
            revers_message = event.text
            write_message(sender, "Ок", keyboard)"""



if __name__ == "__main__":
    main()