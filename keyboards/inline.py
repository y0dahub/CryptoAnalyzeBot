from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

async def generate_pairs_kb(names):
    markup = InlineKeyboardBuilder()

    for name in names:
        markup.add(InlineKeyboardButton(text=f"{name}", callback_data=f"P_{name}"))
    markup.adjust(2)

    return markup.as_markup()

