import asyncio

from aiogram.fsm.context import FSMContext

from app.forms.requests import refresh_token
from logs.logger import logger


async def refresh_access_token(state: FSMContext):
    while True:
        await asyncio.sleep(3600)  # 3600 -> 1 час

        user_data = await state.update_data()
        token = user_data.get("refresh_token")

        if token:
            access_token = await refresh_token(token)
            if access_token:
                await state.update_data(access_token=token)
                logger.success("Access token успешно обновлен")
            else:
                logger.error("Не удалось обновить access token")
        else:
            logger.error("Refresh token отсутствует")
