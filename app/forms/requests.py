from aiogram.fsm.context import FSMContext
from httpx import AsyncClient


async def sign_in(username: str,
                  password: str,
                  state: FSMContext):
    url = "http://127.0.0.1:8080/api/v1/auth/restaurants-editors/sign_in/"

    form_data = {
        "username": username,
        "password": password
    }

    async with AsyncClient() as client:
        response = await client.post(url, data=form_data)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            try:
                error_data = response.json()
            except ValueError:
                return f"Internal server error: {response.status_code} {response.text}"
        return error_data


async def refresh_token(refresh_token: str):
    url = f"http://127.0.0.1:8080/api/v1/restaurants-editors/token/refresh/{refresh_token}"

    params = {
        "refresh_token": refresh_token
    }

    async with AsyncClient() as client:
        response = await client.post(url=url, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                return data.get("access_token")
            except ValueError:
                return None
        else:
            return f"Internal server error: {response.status_code} {response.text}"
