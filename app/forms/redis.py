from config.database import get_redis_connection, close_redis_connection
from logs.logger import logger


# user_id -> user_id телеграмма
async def set_is_logged_in(user_id: str, is_logged_in: bool):
    try:
        redis = await get_redis_connection()
        await redis.set(f"User with ID: {user_id} is logged in", str(is_logged_in))
        logger.success("Пользователь с ID: %s успешно вошел в аккаунт", user_id)
    except Exception as e:
        logger.error("Произошла ошибка: %s при сохранение пользователя с UUID: %s", e, user_id)
    finally:
        await close_redis_connection()


async def get_is_logged_in(user_id: str):
    try:
        redis = await get_redis_connection()
        status = await redis.get(f"User with ID: {user_id} is logged in")
        logger.success("Пользователь с UUID: %s уже авторизованный")
        return status == "True"
    except Exception as e:
        logger.error("Произошла ошибка: %s при получение пользователя с ID: %s", e, user_id)
    finally:
        await close_redis_connection()
