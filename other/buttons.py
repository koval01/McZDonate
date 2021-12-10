from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_text = "Отмена"
cancel.add(KeyboardButton(cancel_text))


async def create_inline_buttons(buttons) -> dict:
    """Функция генерации Inline клавиатуры"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for key in buttons: keyboard.add(KeyboardButton(key))
    return keyboard
