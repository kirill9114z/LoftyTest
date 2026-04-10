from sys import argv
import asyncio

from config import get_config
from weather_method import get_weather
from session_weather import get_session, close_session



async def main():
    lst_args = argv[1:]
    city = lst_args[0]
    settings = get_config()
    session = await get_session()
    result = await get_weather(city, session, settings)
    if result["ok"]:
        text_weather = f'В городе {city} {result["weather"]} и {result['temp']}°C градусов {"тепла" if int(result['temp']) > 0 else "мороза"}'
    else:
        text_weather = result['details']
    print(text_weather)
    await close_session()
    return text_weather

if __name__ == "__main__":
    asyncio.run(main())