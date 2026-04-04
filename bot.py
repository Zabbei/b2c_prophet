import telebot
import random
from telebot import types
import os
from flask import Flask
import threading

# Получаем секретный ключ бота
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# НАШИ ВОПРОСЫ И ОТВЕТЫ
# Ты можешь менять текст в кавычках на свой!
qa_data = {
    "Что меня ждет сегодня?": [
        "Сегодня будет потрясающий день!",
        "Возможны мелкие хлопоты, но ты со всем справишься.",
        "Жди приятных новостей к вечеру!"
    ],
    "Что мне съесть?": [
        "Купи себе самую вкусную пиццу.",
        "Сделай легкий и полезный салат.",
        "Сегодня день для сладкого, побалуй себя десертом!"
    ],
    "Смотреть ли фильм?": [
        "Обязательно посмотри! Отличная идея.",
        "Лучше проведи время за хорошей книгой.",
        "Да, только выбери смешную комедию."
    ]
}

# Реакция на команду /start (когда пользователь запускает бота)
@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Автоматически делаем кнопки из наших вопросов
    for question in qa_data.keys():
        markup.add(types.KeyboardButton(question))
   
    bot.send_message(
        message.chat.id,
        "Привет! Выбери интересующий тебя вопрос на клавиатуре ниже:",
        reply_markup=markup
    )

# Реакция на текст (когда пользователь нажимает кнопку)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    question = message.text
    # Если вопрос есть в нашем списке
    if question in qa_data:
        # Выбираем случайный ответ из списка ответов для этого вопроса
        answer = random.choice(qa_data[question])
        bot.send_message(message.chat.id, answer)
    else:
        # Если написали что-то другое
        bot.send_message(message.chat.id, "Пожалуйста, нажми на кнопку с вопросом внизу экрана.")

# --- Служебный код для сервиса Render ---
# Это нужно, чтобы бесплатный сервер не отключал нашего бота
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот успешно работает!"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
