import telebot
from telebot import types
import os

bot = telebot.TeleBot("7627350184:AAFbHsauSaJiSagGTL_aWyrm9G0_Gdncc5M")
user_data = {}

# Наши константы)
PHOTO_URL = "https://i.pinimg.com/736x/51/22/35/5122357bebc8b91e7dc276a04491a446.jpg"
TEXT_FILE = 'mjk1_text.txt'
ROUTE_FILE = 'route_text.txt'

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🏘️ МЖК-1 г. Свердловска / микрорайон «Комсомольский»")
    btn2 = types.KeyboardButton("От последние <<Рубежи>> МЖК-1 до Долина Холмов")
    btn3 = types.KeyboardButton("Перейти на карту")
    btn4 = types.KeyboardButton("📞 Контакты организаторов")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(func=lambda message: message.chat.id not in user_data)
def welcome_new_user(message):
    chat_id = message.chat.id
    user_data[chat_id] = True  # Помечаем пользователя как "зарегистрированного"

    bot.send_photo(chat_id, PHOTO_URL,
                   caption="🏞️ Добро пожаловать в информационный бот парковых проектов! Выберите интересующий вас раздел:",
                   reply_markup=main_menu(chat_id))


def load_text_from_file(filename):
    """Загружает текст из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return "Текст временно недоступен. Пожалуйста, попробуйте позже."
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return "Произошла ошибка при загрузке текста."

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    if text == "🏘️ МЖК-1 г. Свердловска / микрорайон «Комсомольский»":
        route_info = load_text_from_file(ROUTE_FILE)
        bot.send_message(chat_id, route_info, parse_mode='HTML')
    elif text == "От последние <<Рубежи>> МЖК-1 до Долина Холмов":
        route_text = load_text_from_file(TEXT_FILE)
        bot.send_message(chat_id, route_text,parse_mode='HTML')

    elif text == "Перейти на карту":
        bot.send_message(chat_id, "🌍 Карта маршрута: https://www.google.com/maps/d/edit?mid=1-C_a8bh1yb_brR_hjOQMhZQjc8rMQS0&usp=sharing")

    elif text == "📞 Контакты организаторов":
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Группа ВКонтакте", url="https://vk.com/ano_mestnye"))
        markup.row(types.InlineKeyboardButton("Канал Telegram", url="https://t.me/ano_mestnye"))
        bot.send_message(chat_id, "Для проектов по МЖК и Комсомольскому:\n\nРаботу по туристической популяризации МЖК-1 ведёт АНО «Местные».", reply_markup=markup)


if __name__ == "__main__":
    bot.polling(none_stop=True)