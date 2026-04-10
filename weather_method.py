from typing import Any

from session_weather import request
from aiohttp import ClientSession
from config import Config
from storage import set_coordinates, get_coordinates


async def get_lat_lon(city_name: str, session: ClientSession, setting: Config) -> dict[Any, Any]:
    url = f"{setting.BASE_URL}/geo/1.0/direct?q={city_name}&limit=1&appid={setting.API_KEY}&lang"
    result = await request(session, url, setting)

    if not result["ok"]:
        if result["status"] == 401:
            return {"ok": False, "details": "Invalid API Key"}
        return {"ok": False, "details": result.get("error", f"Unknown Error Response: {result['status']}")}

    data = result["data"]
    if not data:
        return {"ok": False, "details": f"City '{city_name}' not found"}

    return {"ok": True, "details": {"lat": data[0]["lat"], "lon": data[0]["lon"]}}


async def get_weather(city_name: str, session: ClientSession, setting: Config):
    coordinates = get_coordinates(city=city_name)
    if coordinates:
        url = f"{setting.BASE_URL}/data/2.5/weather?lat={coordinates['details']['lat']}&lon={coordinates['details']['lon']}&units=metric&lang=ru&appid={setting.API_KEY}"
    else:
        coordinates = await get_lat_lon(city_name=city_name, session=session, setting=setting)
        if coordinates['ok']:
            set_coordinates(city=city_name, coordinates=coordinates)
            url = f"{setting.BASE_URL}/data/2.5/weather?lat={coordinates['details']['lat']}&lon={coordinates['details']['lon']}&units=metric&lang=ru&appid={setting.API_KEY}"
        else:
            return coordinates

    result = await request(session, url, setting)

    if not result["ok"]:
        return {"ok": False, "details": result.get("error", result.get("data"))}

    data = result["data"]
    weather = {"ok": True,"weather": data["weather"][0]["description"], "temp": data["main"]["temp"]}
    return weather