from httpx import AsyncClient


async def set_language(language: str):
    url = f"http://127.0.0.1:8080/api/v1/language/{language}/"

    async with AsyncClient() as client:
        response = await client.post(url=url)

    if response.status_code == 200:
        return response.json().get("detail")

    else:
        return f"Ошибка: {response.status_code}, {response.text}"
