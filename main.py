import logging
import json
from types import SimpleNamespace

import telebot
from telebot import types

with open('settings.json') as file:
    settings = SimpleNamespace(**json.load(file))
admin_id = settings.ADMIN_ID
bot = telebot.TeleBot(settings.API_TOKEN)

#logging init
logging.basicConfig()
logger = logging.getLogger('feedback bot')
logger.setLevel(logging.INFO)

# log about bot
bot_info = '\n' + '\n'.join(f"{(k+':').ljust(14)}  {v}" for k, v in 
                            bot.get_me().__dict__.items())
logger.info(bot_info)


@bot.message_handler(commands=['start', 'help'])
def hello(message):
    try:
        if message.chat.id == admin_id:
            bot.send_message(admin_id, settings.HELLO_ADMIN)
        else:
            bot.send_message(message.chat.id, settings.HELLO_CHAT)
    except:
        logger.exception('Sending Error!')


@bot.message_handler(func=lambda mess: mess.from_user.id == admin_id)
def handle_admin_messages(message: types.Message):
    if message.reply_to_message is None:
        try:
            bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)
        except:
            logger.exception('Sending Error')
        return
    try:
        chat_id = message.reply_to_message.forward_from.id
        # TODO: add other types
        bot.send_message(chat_id, message.text, parse_mode='Markdown')
    except:
        logger.exception('Replying Error!')

@bot.message_handler(func=lambda mess: mess.from_user.id != admin_id)
def handle_other_messages(message: types.Message):
    try:
        bot.forward_message(admin_id, message.chat.id, message.message_id)
    except:
        logger.exception('Forwarding Error!')


if __name__ == '__main__':
    bot.polling(none_stop=True,  interval=1)
