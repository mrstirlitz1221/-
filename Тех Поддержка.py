import telebot


TOKEN = "6078482054:AAFk71CCk4ySum3DAB2vzF1sVnWG_IlqCzc"
bot = telebot.TeleBot(TOKEN)

USERS_FILE = 'users.txt'

ADMIN_CHAT_ID = 1138500722

try:
    with open("pod.txt", "r") as handle:
        file_contents = handle.read()
        exec("database = " + file_contents)
except:
    database = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_name = message.from_user.first_name
    add_user_to_database(user_id, username, user_name)
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет ✌️\nC моей помощью ты можешь связаться с моим хозяином и получить от него ответ. Просто напиши что-нибудь в этот диалог."
    )


def add_user_to_database(user_id, username, user_name=None):
    if user_id not in database:
        database[user_id] = {
            'name': user_name,
            'user': username,
        }
        with open("pod.txt", "w+") as handle:
            handle.write(str(database))

@bot.message_handler(commands=['see'])
def see_user(message):
    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)
    if message.from_user.id == ADMIN_CHAT_ID:
        if database:
            text = ""
            for user_id, user_data in database.items():
                text = f"ID: {user_id}\nUser: {user_data['user']}\nName: {user_data['name']}"
                bot.send_message(chat_id=message.chat.id, text=text)
        else:
            bot.send_message(chat_id=message.chat.id, text="Нечего нет")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")


@bot.message_handler(commands=['ras'])
def broadcast(message):
    if message.from_user.id == ADMIN_CHAT_ID:
        message_text = message.text.replace("/ras ", "")
        for user_id in database:
            try:
                bot.send_message(user_id, message_text)
            except:
                bot.send_message(chat_id=message.chat.id, text=f"Не удалось отправить сообщение пользователю с идентификатором: {user_id}")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")

@bot.message_handler(commands=['r'])
def message_user(message):
    if message.from_user.id == ADMIN_CHAT_ID:
        message_text = message.text.replace("/r ", "")
        user_id = message_text.split(" ")[0]
        message_text = message_text.replace(user_id + " ", "")
        try:
            bot.send_message(user_id, message_text)
            bot.send_message(chat_id=message.chat.id, text=f"Сообщение отправлено пользователю с id: {user_id}")
        except:
            bot.send_message(chat_id=message.chat.id, text=f"Не удалось отправить сообщение пользователю с идентификатором: {user_id}")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")

@bot.message_handler(func=lambda message: True)
def customer_support_handler(message):
    bot.forward_message(
        chat_id='1138500722',
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Спасибо за ваше сообщение. Наша служба поддержки свяжется с вами в ближайшее время."
    )
    bot.send_message(
        chat_id='1138500722',
        text=f"Новый запрос в службу поддержки от {message.chat.username or message.chat.first_name} ({message.chat.id}):\n{message.text}"
    )


bot.polling(none_stop=True, interval=0)
