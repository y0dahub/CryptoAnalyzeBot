from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from utils.database.database import Database
from utils.crypto.bybit import BybitApi
from utils.conditions.funcs import validate_condition, evaluate_condition
from forms.forms import TaskForm
from config import HOST

import asyncio

router = Router()
db = Database(host=HOST)
bybit = BybitApi()


async def track_task(user_id, task_id, currency_pair, condition):
    while True:
        current_price = await bybit.get_cost(symbol=currency_pair, type_of_cost="indexPrice")

        if evaluate_condition(current_price=current_price, condition=condition):
            await db.complete_task(user_id=user_id, task_id=task_id)

            return [f"Условие выполнено! Текущая цена {currency_pair}: {current_price}", True]

        await asyncio.sleep(5)


@router.callback_query(F.data.startswith("P_"))
async def get_currency(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    curr = f"{callback.data.split('_')[1]}"

    await state.update_data({"currency_pair": curr})
    await state.set_state(TaskForm.task_condition)
    await callback.message.answer("Введи условие, которое будет отслеживать бот\n\nex. >5000")


@router.message(TaskForm.task_condition)
async def get_condition(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data({"task_condition": message.text})

    if validate_condition(condition=message.text):
        data = await state.get_data()
        currency_pair = data.get("currency_pair")
        task_condition = data.get("task_condition")

        task_id = await db.add_task(
            user_id=message.from_user.id, 
            currency_pair=currency_pair,
            condition=task_condition
        )
        if task_id:
            await message.answer("Задача успешно добавлена.")
            result = await track_task(message.from_user.id, task_id, currency_pair, task_condition)

            await message.answer(result[0])

        else:
            await message.answer("Не удалось добавить задачу.")
    else:
        await message.answer("Условие написано неправильно, должны присутствовать только символы '>', '<', '=' и числа.")
