import logging
import asyncio
import aiogram
from aiogram import Bot, Dispatcher,types 
from aiogram.types import BotCommand

from aiogram import Bot, Dispatcher

from config import TOKEN

from app.database.models import async_main

from app.handlers import router
from app.admin import admin
from app.menu_commands import set_main_menu


bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.startup.register(set_main_menu)


async def main():
    await async_main()
    dp.include_routers(admin, router)
    await dp.start_polling(bot, skip_updates=False)

if __name__ =='__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')