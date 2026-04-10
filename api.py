import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city: str) -> dict:
    """Holt aktuelle Wetterdaten für eine Stadt."""
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_forecast(city: str) -> dict:
    """Holt 5-Tage-Vorhersage (alle 3 Stunden) für eine Stadt."""
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def parse_forecast(data: dict) -> list:
    """Gibt eine vereinfachte Liste der täglichen Vorhersagen zurück."""
    daily = {}
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = {
                "date": date,
                "temp_min": entry["main"]["temp_min"],
                "temp_max": entry["main"]["temp_max"],
                "description": entry["weather"][0]["description"],
                "icon": entry["weather"][0]["icon"],
                "humidity": entry["main"]["humidity"],
                "wind": entry["wind"]["speed"],
                "temps": []
            }
        daily[date]["temps"].append(entry["main"]["temp"])
        daily[date]["temp_min"] = min(daily[date]["temp_min"], entry["main"]["temp_min"])
        daily[date]["temp_max"] = max(daily[date]["temp_max"], entry["main"]["temp_max"])

    return list(daily.values())[:5]