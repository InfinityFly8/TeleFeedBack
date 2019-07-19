from aiogram import Bot, types
from parameters import logger, settings
from db_control import Banlist
ADMIN_ID = settings.ADMIN_ID

banlist = Banlist()

# logs info about the bot
async def log_bot_info(bot: Bot):
    bot_info = await bot.get_me()
    bot_str = '\n' + '\n'.join(f"{(k+':').ljust(14)}  {v}" for k, v in 
                                bot_info.values.items())
    logger.info(bot_str)


class AllTypes:
    def __contains__(*args):
        return True


def is_admin(message: types.Message):
    return message.from_user.id == ADMIN_ID


def is_not_admin(message: types.Message):
    id = message.from_user.id
    return id != ADMIN_ID and id not in banlist


#resend any message to id
async def send_message_content(bot: Bot, id, message: types.Message):
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
        await bot.send_message(ADMIN_ID, settings.UNSUPPORTED_TYPE)