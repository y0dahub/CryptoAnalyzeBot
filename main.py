from aiogram import Bot, Dispatcher

from asyncio import run
from config import TOKEN

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)