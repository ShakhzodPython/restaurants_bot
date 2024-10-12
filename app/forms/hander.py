from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from languages.translation import get_translation, get_user_language
from app.forms.requests import sign_in

router_sign_in = Router()


class SignInForm(StatesGroup):
    username = State()
    password = State()


@router_sign_in.message(Command(commands=["sign_in"]))
async def sign_in_command(message: Message, state: FSMContext):
    lang = await get_user_language(state)
    enter_username_msg = get_translation(lang, "enter_username")
    await message.answer(text=enter_username_msg, reply_markup=ReplyKeyboardRemove())

    await state.set_state(SignInForm.username)


@router_sign_in.message(SignInForm.username)
async def enter_username_command(message: Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)

    lang = await get_user_language(state)
    enter_password_msg = get_translation(lang, "enter_password")
    await message.answer(text=enter_password_msg)

    await state.set_state(SignInForm.password)


@router_sign_in.message(SignInForm.password)
async def enter_password_command(message: Message, state: FSMContext):
    password = message.text

    user_data = await state.get_data()
    username = user_data.get("username")

    await state.clear()
