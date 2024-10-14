import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.forms.utils import refresh_access_token
from languages.translation import get_translation, get_user_language
from app.forms.requests import sign_in

router_authorization = Router()


class SignInForm(StatesGroup):
    username = State()
    password = State()


@router_authorization.message(Command(commands=["sign_in"]))
async def sign_in_command(message: Message, state: FSMContext):
    user_data = await state.get_data()
    is_logged_in = user_data.get("is_logged_in", False)

    lang = await get_user_language(state)

    if is_logged_in == False:
        already_logged_in_msg = get_translation(lang, "already_logged_in")
        await message.answer(text=already_logged_in_msg)
        return

    enter_username_msg = get_translation(lang, "enter_username")
    await message.answer(text=enter_username_msg, reply_markup=ReplyKeyboardRemove())
    await asyncio.create_task(refresh_access_token(state))

    await state.set_state(SignInForm.username)


@router_authorization.message(SignInForm.username)
async def enter_username_command(message: Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)

    lang = await get_user_language(state)
    enter_password_msg = get_translation(lang, "enter_password")
    await message.answer(text=enter_password_msg)

    await state.set_state(SignInForm.password)


@router_authorization.message(SignInForm.password)
async def enter_password_command(message: Message, state: FSMContext):
    password = message.text

    user_data = await state.get_data()
    username = user_data.get("username")

    response = await sign_in(username, password)
    if response:
        await state.update_data(is_logged_in=True)  # Устанавливаем флаг, что пользователь вошел в аккаунт
        await message.answer(text=response)
    else:
        await message.answer(text="Ошибка входа. Проверьте имя пользователя или пароль")

    await state.clear()


@router_authorization.message(Command(commands=["log_out"]))
async def log_out():
    pass
