import asyncio
import os
import config
import sys
import logging
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from pytube import YouTube

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer('Для скачивания видео пропишите /download "ссылка"')
@dp.message(Command('download'))
async def command_download_handler(message: Message):
    try:
        video_url = message.text.split()[1]
        save_path = "./video"
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

        yt = YouTube(video_url)
        stream = yt.streams.filter(resolution='720p', progressive=True).first()
        video_file = stream.download(output_path=save_path)

        await message.answer(f"Видео '{yt.title}' успешно загружено!")

        with open(video_file, 'rb') as v:
            await bot.send_video(chat_id=message.chat.id, video=v)

        os.remove(video_file)

        await message.answer("Видео успешно отправлено и удалено с сервера.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
async def main():
    global dp
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())