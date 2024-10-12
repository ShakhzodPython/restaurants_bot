import json

from aiogram.fsm.context import FSMContext

# Загрузка перевода из JSON
with open("languages/translations.json", "r", encoding="utf-8") as file:
    translations = json.load(file)


# Функция для получения перевода
def get_translation(lang, key):
    return translations.get(lang, {}).get(key, key)


async def get_user_language(state: FSMContext) -> str:
    user_data = await state.get_data()
    return user_data.get("lang")
