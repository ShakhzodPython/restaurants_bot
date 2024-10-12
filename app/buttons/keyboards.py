from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from languages.translation import get_translation


async def choose_lang():
    btn = [
        [KeyboardButton(text="Русский 🇷🇺")],
        [KeyboardButton(text="O'zbekcha 🇺🇿")]
    ]
    # Передаем кнопки в параметр `keyboard`
    keyboard = ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    return keyboard


async def sign_in(lang):
    sign_in_msg = get_translation(lang, "sign_in")
    btn = [[KeyboardButton(text=sign_in_msg)]]
    keyboard = ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    return keyboard
