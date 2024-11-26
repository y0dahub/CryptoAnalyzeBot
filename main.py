from aiogram import Bot, Dispatcher

from asyncio import run

from handlers import user_commads, user_messages, curr
from config import TOKEN

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(
        user_commads.router,
        user_messages.router,
        curr.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())