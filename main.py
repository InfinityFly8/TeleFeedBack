import asyncio
import logging

import emoji
import aiogram
from aiogram import executor, types, Bot, Dispatcher

from parameters import settings, banlist
admin_id = settings.ADMIN_ID

bot = Bot(settings.API_TOKEN)
dp = Dispatcher(bot)

#logging init
logging.basicConfig()
logger = logging.getLogger('feedback bot')
logger.setLevel(logging.INFO)

# log about bot
async def log_bot_info():
    bot_info = await bot.get_me()
    bot_str = '\n' + '\n'.join(f"{(k+':').ljust(14)}  {v}" for k, v in 
                                bot_info.values.items())
    logger.info(bot_str)
asyncio.gather(log_bot_info())

# helper snippets
class AllTypes:
    def __contains__(*args):
        return True

def is_admin(message: types.Message):
    return message.from_user.id == admin_id

def is_not_admin(message: types.Message):
    id = message.from_user.id
    return id != admin_id and id not in banlist


#resend any message to id
async def send_message_content(id, message: types.Message):
    # text, audio, document, photo, sticker, video, video_note, voice, invoice
    if message.content_type == 'text':
        await bot.send_message(id, message.text)

    elif message.content_type == 'audio':
        await bot.send_audio(id, message.audio.file_id, caption=message.caption)

    elif message.content_type == 'document':
        await bot.send_document(id, message.document.file_id, caption=message.caption)

    elif message.content_type == 'photo':
        await bot.send_photo(id, message.photo[-1].file_id, caption=message.caption)

    elif message.content_type == 'sticker':
        await bot.send_sticker(id, message.sticker.file_id)

    elif message.content_type == 'video':
        await bot.send_video(id, message.video.file_id, caption=message.caption)

    elif message.content_type == 'video_note':
        await bot.send_video_note(id, message.video_note.file_id)

    elif message.content_type == 'voice':
        await bot.send_voice(id, message.voice.file_id, caption=message.caption)

    elif message.content_type == 'invoice':
        await bot.send_invoice(id, message.invoice.file_id)
    else:
        await bot.send_message(admin_id, settings.UNSUPPORTED_TYPE)
    

# commands handlers
@dp.message_handler(commands=['start', 'help'])
async def hello(message):
    try:
        if message.chat.id == admin_id:
            await bot.send_message(admin_id, settings.HELLO_ADMIN)
        else:
            await bot.send_message(message.chat.id, settings.HELLO_CHAT)
    except:
        logger.exception('Sending Error!')


@dp.message_handler(is_admin, commands=['ban'])
async def ban_user(message):
    if message.reply_to_message is None:
        try:
            logger.info('No reply')
            await bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)
        except:
            logger.exception('Sending Error')
        return
    try:
        id = message.reply_to_message.forward_from.id
        logger.info('User %s banned' % id)
        banlist.add(id)
        await bot.send_message(admin_id, settings.USER_IS_BANNED)
        await bot.send_message(id, settings.YOU_ARE_BANNED)
    except:
        logger.exception('Banning error')


# handle messages from admin and send it to replyed user
@dp.message_handler(is_admin, content_types=AllTypes())
async def handle_admin_messages(message):
    logger.info('New message from admin')
    if message.reply_to_message is None:
        try:
            logger.info('No reply')
            await bot.send_message(admin_id, settings.NO_REPLY_MESSAGE)

        except:
            logger.exception('Sending Error')
        return
    try:
        chat_id = message.reply_to_message.forward_from.id
        if chat_id in banlist:
            await bot.send_message(admin_id, settings.USER_IS_BANNED)
        else:
            await send_message_content(chat_id, message)
        logger.info('Send message to user')
    except:
        logger.exception('Replying Error!')


# handle messages from anyone and send it to admin
@dp.message_handler(is_not_admin, content_types=AllTypes())
async def handle_other_messages(message):
    logger.info('New message')
    try:
        await bot.forward_message(admin_id, message.chat.id, message.message_id)
        logger.info('Send message to admin')
    except:
        logger.exception('Forwarding Error!')


if __name__ == '__main__':
    executor.start_polling(dp)
