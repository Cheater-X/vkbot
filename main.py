import random
import sqlite3
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor
import datetime
from datetime import date


def main():
    "Ключ для работы с vk_api"
    token = "vk1.a.ks1r-nPDKh57EgLcAdr3KSf50HSWQc48niM3rqsondwyswzfdbCATJV0Y5s4rooHfMBzWIen6fWVkveiexkTC6DsLLGWV_fpJuwpjYPHV14-SAyTNloslO0K82FqDWEQL_lsgjE5zDjV8Ogxj0e9ofYgwMQyBitc6zEIIKRqMFv4Ui54cOSWcT5UnV3e9cMOqy1G9PWkOnLVscYEhtHRwA"
    vk_sesion = vk_api.VkApi(token=token)  #подключение ключа к версии Vk-api
    "Подключение версии Vk-api к сообществу"
    longpoll = VkBotLongPoll(vk_sesion, "224556618")
    flag = 0
    "Работа с мероприятиями"
    for event in longpoll.listen():
        "Если поступает новое сообщение"
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_sesion.get_api()
            user_message = event.obj.message["text"]
            if user_message != "Войти" and flag == 0:
                keyboard = VkKeyboard(one_time=True, inline=False)
                keyboard.add_button("Войти", color=VkKeyboardColor.PRIMARY)
                vk.messages.send(user_id=event.obj.message["from_id"],
                                 message="Доброго времени суток. Чтобы начать работу в боте авторизуйтесь или зарегестрируйтесь.",
                                 random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())
            elif user_message == "Войти":
                flag = flag + 1
                vk.messages.send(user_id=event.obj.message["from_id"],
                                message="Вы успешно авторизовались в боте. Чтобы продолжить работу введите /help",
                                random_id=random.randint(0, 1000000000))
                user = event.obj.message["from_id"]
                user_ids = vk.users.get(user_id=user)
                user_get = user_ids[0]
                first_name = user_get["first_name"]
                last_name = user_get["last_name"]
                print(first_name, last_name)
                registr_info(user, first_name, last_name)
                try:
                    flag = flag + 1
                except TypeError as f:
                    print(f)
            elif flag >= 2:
                if user_message == "/help":
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_button("Посмотреть статистику", color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button("Предложения по улучшению", color=VkKeyboardColor.PRIMARY)
                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message="Список доступных возможностей:",
                                     random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())
                elif user_message == "Посмотреть статистику":
                    user = event.obj.message["from_id"]
                    con = sqlite3.connect("regbasa.db.sqlite")  #подключение к бд в которой будут данные пользователя
                    cur = con.cursor()
                    cur.execute(f"""SELECT date, time FROM reginfo WHERE id = '{user}'""")
                    data = cur.fetchone()
                    cur.execute(f"""SELECT id FROM reginfo WHERE id = '{user}'""")
                    id = cur.fetchone()
                    cur.execute(f"""SELECT name FROM reginfo WHERE id = '{user}'""")
                    name = cur.fetchone()
                    cur.execute(f"""SELECT last_name FROM reginfo WHERE id = '{user}'""")
                    la_name = cur.fetchone()
                    con.commit()
                    con.close()

                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message=f"Дата регистрации в боте: {data}\nid: {id}\nИмя: {name}\nФамилия: {la_name}",
                                     random_id=random.randint(0, 1000000000))
                elif user_message == "Предложения по улучшению":
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_button("Написать предложение по улучшению", color=VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button("Список предложений по улучшению", color=VkKeyboardColor.SECONDARY)
                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message=f"Выберите раздел: ",
                                     random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())
                elif user_message == "Написать предложение по улучшению":
                    flag = flag + 1
                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message=f"Напишите ниже своё предложение по улучшению",
                                     random_id=random.randint(0, 1000000000))
                elif flag >= 3 and user_message != "Назад":
                    keyboard = VkKeyboard(one_time=True, inline=False)
                    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message=f"Предолжение по улучшению отправлено.\n"
                                             f" Спасибо за обращение.\n "
                                             f"Если у вас есть ещё предложение напишите их ниже.\n"
                                             f"Если предложений нет, можете вернуться назад",
                                     random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())
                    text_add = user_message
                    con = sqlite3.connect("regbasa.db.sqlite")
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO predlozh(add_predlozh) VALUES('{text_add}')")  #подключение к табл с предложениями

                    con.commit()
                    con.close()
                elif user_message == "Список предложений по улучшению":
                    if user_get["id"] != 594755781:
                        keyboard = VkKeyboard(one_time=True, inline=False)
                        keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                        vk.messages.send(user_id=event.obj.message["from_id"],
                                    message=f"У вас нет доступа к просматриванию списка предложений по улучшению\n:)",
                                    random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())
                    else:
                        con = sqlite3.connect("regbasa.db.sqlite")
                        cur = con.cursor()
                        cur.execute(f"""SELECT add_predlozh FROM predlozh""")
                        dannie = cur.fetchall()
                        k = 0
                        for i in dannie:
                            k = k + 1
                            vk.messages.send(user_id=event.obj.message["from_id"],
                                             message=f"{k}.{i}",
                                             random_id=random.randint(0, 1000000000))
                elif user_message == "Назад":
                    flag = flag - 1
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_button("Посмотреть статистику", color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button("Предложения по улучшению", color=VkKeyboardColor.PRIMARY)
                    vk.messages.send(user_id=event.obj.message["from_id"],
                                     message="Список доступных возможностей:",
                                     random_id=random.randint(0, 1000000000), keyboard=keyboard.get_keyboard())

            else:
                pass

"регистрация"
def registr_info(user, first_name, last_name):
    try:
        today = str(date.today())
        current_time = datetime.datetime.now().time()
        time = str(current_time)
        time_today = str(time[:8])
        con = sqlite3.connect("regbasa.db.sqlite")
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO reginfo(date, time, id, name, last_name) VALUES('{today}','{time_today}','{user}', '{first_name}', '{last_name}')")

        con.commit()
        con.close()
    except vk_api.AuthError as error_msg:
        print(error_msg)

"Запуск"
if __name__ == "__main__":
    main()