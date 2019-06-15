import logging

import emoji
import telebot
from telebot import types

from parameters import settings, banlist
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

# helper snippets
class AllTypes:
    def __contains__(*args):
        return True

def is_admin(message):
    return message.from_user.id == admin_id

def is_not_admin(message):
    id = message.from_user.id
    return id != admin_id and id not in banlist


#resend any message to id
def send_message_content(id, message):
    # text, audio, document, photo, sticker, video, video_note, voice, invoice
    if message.content_type == 'text':
        bot.send_message(id, message.text)

    elif message.content_type == 'audio':
        bot.send_audio(id, message.audio.file_id, caption=message.caption)

    elif message.content_type == 'document':
        bot.send_document(id, message.document.file_id, caption=message.caption)

    elif message.content_type == 'photo':
        bot.send_photo(id, message.photo[-1].file_id, caption=message.caption)

    elif message.content_type == 'sticker':
        bot.send_sticker(id, message.sticker.file_id)

    elif message.content_type == 'video':
        bot.send_video(id, message.video.file_id, caption=message.caption)

    elif message.content_type == 'video_note':
        bot.send_video_note(id, message.video_note.file_id)

    elif message.content_type == 'voice':
        bot.send_voice(id, message.voice.file_id, caption=message.caption)

    elif message.content_type == 'invoice':
        bot.send_invoice(id, message.invoice.file_id)
    else:
        bot.send_message(admin_id, settings.UNSUPPORTED_TYPE)
    

# commands handlers
@bot.message_handler(commands=['start', 'help'])
def hello(message):
    try:
        if message.chat.id == admin_id:
            bot.send_message(admin_id, settings.HELLO_ADMIN)
        else:
            bot.send_message(message.chat.id, settings.HELLO_CHAT)
    except:
        logger.exception('Sending Error!')


@bot.message_handler(commands=['ban'], func=is_admin)
def ban_user(message):
    if message.reply_to_message is None:
        try:
            logger.info('No reply')
            bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)
        except:
            logger.exception('Sending Error')
        return
    try:
        id = message.reply_to_message.forward_from.id
        logger.info('User %s banned' % id)
        banlist.add(id)
        bot.send_message(admin_id, settings.USER_IS_BANNED)
        bot.send_message(id, settings.YOU_ARE_BANNED)
    except:
        logger.exception('Banning error')


# handle messages from admin and send it to replyed user
@bot.message_handler(func=is_admin, content_types=AllTypes())
def handle_admin_messages(message):
    logger.info('New message from admin')
    if message.reply_to_message is None:
        try:
            logger.info('No reply')
            bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)
        except:
            logger.exception('Sending Error')
        return
    try:
        chat_id = message.reply_to_message.forward_from.id
        if chat_id in banlist:
            bot.send_message(admin_id, settings.USER_IS_BANNED)
        else:
            send_message_content(chat_id, message)
        logger.info('Send message to user')
    except:
        logger.exception('Replying Error!')


# handle messages from anyone and send it to admin
@bot.message_handler(func=is_not_admin, content_types=AllTypes())
def handle_other_messages(message):
    logger.info('New message')
    try:
        bot.forward_message(admin_id, message.chat.id, message.message_id)
        logger.info('Send message to admin')
    except:
        logger.exception('Forwarding Error!')


if __name__ == '__main__':
    bot.polling(none_stop=True,  interval=1)
