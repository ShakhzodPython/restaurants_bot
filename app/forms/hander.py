import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.forms.redis import set_is_logged_in, get_is_logged_in
from app.forms.utils import refresh_access_token
from languages.translation import get_translation, get_user_language
from app.forms.requests import sign_in

router_authorization = Router()


class SignInForm(StatesGroup):
    username = State()
    password = State()


@router_authorization.message(Command(commands=["sign_in"]))
async def sign_in_command(message: Message, state: FSMContext):
    lang = await get_user_language(state)

    # Проверка пользователя авторизован ли он
    user_id = message.from_user.id
    is_logged_in = await get_is_logged_in(str(user_id))
    if is_logged_in:
        already_logged_in_msg = get_translation(lang, "already_logged_in")
        await message.answer(text=already_logged_in_msg, reply_markup=ReplyKeyboardRemove())
    else:
        enter_username_msg = get_translation(lang, "enter_username")
        await message.answer(text=enter_username_msg, reply_markup=ReplyKeyboardRemove())

    asyncio.create_task(refresh_access_token(state))

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

    response = await sign_in(username, password, state)

    access_token = response.get("access_token")
    if access_token:
        user_id = str(message.from_user.id)
        await set_is_logged_in(user_id, True)
        await message.answer(text=response.get("detail"))
    else:
        await message.answer(text=response.get("detail"))

    await state.clear()


@router_authorization.message(Command(commands=["log_out"]))
async def log_out():
    pass
