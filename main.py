# TODO: добавить логи
import asyncio

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommand

from app.forms.hander import router_authorization
from languages.requests import set_language
from languages.translation import get_translation
from config.settings import API_TOKEN
from app.buttons.keyboards import choose_lang, sign_in
from app.forms.hander import sign_in_command

router = Router()


class LanguageForm(StatesGroup):
    choosing_language = State()
    expectation = State()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу бота/Botni ishga tushiring"),
        BotCommand(command="/help", description="Помощь/Yordam"),
        BotCommand(command="/change_language", description="Изменить язык/Tilni almashtirish"),
    ]
    await bot.set_my_commands(commands)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    keyboard = await choose_lang()
    await message.answer("Выберите язык/Tilni tanlang", reply_markup=keyboard)
    await state.set_state(LanguageForm.choosing_language)


@router.message(LanguageForm.choosing_language)
async def choose_language_command(message: Message, state: FSMContext):
    if message.text == "Русский 🇷🇺":
        lang = "ru"
    elif message.text == "O'zbekcha 🇺🇿":
        lang = "uz"
    else:
        await message.answer("Пожалуйста, выберите один из предложенных языков")

        # Возвращает lang
        return

    # передаем выбранный язык пользователя на серевер
    await set_language(lang)

    await state.update_data(lang=lang)

    keyboard = await sign_in(lang)
    selected_language_msg = get_translation(lang, "selected_language")
    await message.answer(f"{selected_language_msg}: {message.text}", reply_markup=keyboard)
    await state.set_state(LanguageForm.expectation)  # Ожидание входа


@router.message(LanguageForm.expectation)
async def handle_sign_in(message: Message, state: FSMContext):
    await sign_in_command(message, state)


@router.message(Command(commands=["change_language"]))
async def change_language_command(message: Message, state: FSMContext):
    keyboard = await choose_lang()
    await message.answer("Выберите язык/Tilni tanlang", reply_markup=keyboard)
    await state.set_state(LanguageForm.choosing_language)


async def main():
    dp = Dispatcher()
    bot = Bot(API_TOKEN)

    dp.include_router(router)
    dp.include_router(router_authorization)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
