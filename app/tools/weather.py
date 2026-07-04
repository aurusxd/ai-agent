import os

import requests


def get_weather(city: str):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric"
    respone = requests.get(url,timeout=10)
    respone.raise_for_status()
    data = respone.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    weather = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    return (
        f"Погода в городе {city}:\n"
        f"Температура: {temp}°C\n"
        f"Ощущается как: {feels_like}°C\n"
        f"Описание: {weather}\n"
        f"Ветер: {wind} м/с"
    )
