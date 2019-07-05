import asyncio
import logging
import emoji
import aiogram
from aiogram import executor, types, Bot, Dispatcher
from parameters import logger, settings, banlist
from utils import log_bot_info, AllTypes, is_admin, is_not_admin, send_message_content


ADMIN_ID = settings.ADMIN_ID
bot = Bot(settings.API_TOKEN)
dp = Dispatcher(bot)

asyncio.gather(log_bot_info(bot))


# commands handlers
@dp.message_handler(commands=['start', 'help'])
async def hello(message):
    try:
        if message.chat.id == ADMIN_ID:
            await bot.send_message(ADMIN_ID, settings.HELLO_ADMIN)
        else:
            await bot.send_message(message.chat.id, settings.HELLO_CHAT)
    except:
        logger.exception('Sending Error!')


@dp.message_handler(is_admin, commands=['ban'])
async def ban_user(message):
    if message.reply_to_message is None:
        try:
            logger.info('No reply')
            await bot.send_message(ADMIN_ID, settings.NO_REPLY_MESSAGE)
        except:
            logger.exception('Sending Error')
        return
    try:
        id = message.reply_to_message.forward_from.id
        logger.info('User %s banned' % id)
        banlist.add(id)
        await bot.send_message(ADMIN_ID, settings.USER_IS_BANNED)
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
            await bot.send_message(ADMIN_ID, settings.NO_REPLY_MESSAGE)

        except:
            logger.exception('Sending Error')
        return
    try:
        chat_id = message.reply_to_message.forward_from.id
        if chat_id in banlist:
            await bot.send_message(ADMIN_ID, settings.USER_IS_BANNED)
        else:
            await send_message_content(bot, chat_id, message)
        logger.info('Send message to user')
    except:
        logger.exception('Replying Error!')


# handle messages from anyone and send it to admin
@dp.message_handler(is_not_admin, content_types=AllTypes())
async def handle_other_messages(message):
    logger.info('New message')
    try:
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        logger.info('Send message to admin')
    except:
        logger.exception('Forwarding Error!')


if __name__ == '__main__':
    executor.start_polling(dp)
