# Для запуску бота необхідно в директорії бота створити файл data.py з наступним вмістом:
# API_TOKEN = 'ваш_токен'
# admin_id = 'id_адміністратора'

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import admin_id, API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

user_messages = {}
greeted_users = set()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id].append(message.text)
    
    if user_id not in greeted_users:
        bot.reply_to(message, "Вітаємо! Тут ви можете зв'язатись з оператором. Опишіть свою проблему, і ми скоро відповімо.")
        greeted_users.add(user_id)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Відповісти", callback_data=f"reply_{user_id}"))
    bot.send_message(admin_id, f"Повідомлення від користувача {message.from_user.first_name}:\n{message.text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def callback_reply(call):
    user_id = call.data.split('_')[1]
    msg = bot.send_message(call.from_user.id, f"Введіть відповідь для користувача {user_id}:")
    bot.register_next_step_handler(msg, process_reply_step, user_id)

def process_reply_step(message, user_id):
    bot.send_message(user_id, message.text)
    bot.reply_to(message, "Відповідь надіслано.")

if __name__ == "__main__":
    print("Бот запущений під іменем @temporary_group_bot")
    bot.polling(none_stop=True, interval=0)