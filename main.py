# coding=utf-8
""""
"""
import os

from config import TOKEN, SECRET_TOKEN, TG_TOKEN
from api import FusionBrainAPI
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TG_TOKEN)

prompt = ""


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я могу генерировать изображения совершенно бесплатно!\n/gen <промпт> - сгенерировать\n/help - помощь")


@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, "/gen <промпт> - сгенерировать\n")



@bot.message_handler(commands=['gen'])
def handle_gen_config(message):
    global prompt
    prompt = " ".join(message.text.split()[1:])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Обычный", callback_data="NO STYLE"))
    markup.add(InlineKeyboardButton("Цифровой рисунок", callback_data="DIGITAL PAINTING"))
    markup.add(InlineKeyboardButton("Детализированное фото", callback_data="DETAILED PHOTO"))
    markup.add(InlineKeyboardButton("Аниме", callback_data="ANIME"))
    bot.send_message(message.chat.id, f"Промт: {prompt}\nВыбери стиль", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def gen_img(call):
    style = call.data
    print(style)
    bot.send_message(call.message.chat.id, f"Промт: {prompt}\n Генерация началась")
    sending_msg = bot.send_message(call.message.chat.id, "Изображение генерируется..")
    bot.send_chat_action(call.message.chat.id, 'typing')
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', TOKEN, SECRET_TOKEN)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(f"{prompt}", pipeline_id, style=style)
    api.check_generation(uuid)
    with open("result.png", "rb") as f:
        image = f.read()
    bot.delete_message(call.message.chat.id, sending_msg.message_id)
    bot.send_photo(call.message.chat.id, image, "Изображение готово!")
    os.remove("result.png")


if __name__ == '__main__':
    bot.infinity_polling()