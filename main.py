import json
from types import SimpleNamespace

import telebot
from telebot import types

with open('settings.json') as file:
    settings = SimpleNamespace(**json.load(file))
admin_id = settings.ADMIN_ID
bot = telebot.TeleBot(settings.API_TOKEN)
print(bot.get_me())
# log about bot


@bot.message_handler(commands=['start', 'help'])
def hello(message):
    if message.chat.id == admin_id:
        bot.send_message(admin_id, settings.HELLO_ADMIN)
    else:
        bot.send_message(message.chat.id, settings.HELLO_CHAT)


@bot.message_handler(func=lambda mess: mess.from_user.id == admin_id)
def handle_admin_messages(message: types.Message):
    if message.reply_to_message is None:
        bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)
        return
    chat_id = message.reply_to_message.forward_from.id
    # TODO: add other types
    bot.send_message(chat_id, message.text, parse_mode='Markdown')


@bot.message_handler(func=lambda mess: mess.from_user.id != admin_id)
def handle_other_messages(message: types.Message):
    bot.forward_message(admin_id, message.chat.id, message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True,  interval=1)
