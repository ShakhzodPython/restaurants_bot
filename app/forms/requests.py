from httpx import AsyncClient


async def sign_in(username, password):
    url = "http://127.0.0.1:8000/api/v1/auth/restaurants-editors/sign_in/"

    form_data = {
        "username": username,
        "password": password
    }

    async with AsyncClient() as client:
        response = await client.post(url, data=form_data)

        if response.status_code == 200:
            try:
                data = response.json()
                uuid = data.get("uuid")
                access_token = data.get("access_token")
                refresh_token = data.get("refresh_token")

                return {
                    "uuid": uuid,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            except ValueError:
                return None
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
