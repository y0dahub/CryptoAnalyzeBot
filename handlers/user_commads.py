from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from utils.crypto.bybit import BybitApi
from utils.database.database import Database

from keyboards.inline import generate_pairs_kb
from config import HOST

router = Router()
db = Database(host=HOST)
bybit = BybitApi()

@router.message(CommandStart())
async def start(message: Message):
    names = await bybit.get_currencies()

    markup = await generate_pairs_kb(names=names)
    if await db.add_user(user_id=message.from_user.id):
        await message.answer(
            f"Привет, {message.from_user.full_name}\n",
            reply_markup=markup
        )
    else:
        await message.answer(
            f"Привет, {message.from_user.full_name}\n",
            reply_markup=markup
        )
