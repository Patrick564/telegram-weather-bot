import requests

from .models import WeatherDaily, WeatherDayModel

URL_BASE = "https://api.open-meteo.com/v1/forecast"
HOURLY_PARAMS = "hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,rain,cloudcover,uv_index,is_day&forecast_days=1&timezone=auto"  # noqa
DAILY_PARAMS = "daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,uv_index_clear_sky_max,precipitation_hours,precipitation_probability_max&forecast_days=1&timezone=auto"  # noqa


def weather_daily(lat: float, lon: float) -> WeatherDaily:
    r = requests.get(
        f"{URL_BASE}?latitude={lat}&longitude={lon}&{DAILY_PARAMS}"
    )

    return WeatherDaily(**r.json())


def weather_hourly(lat: float, lon: float) -> WeatherDayModel:
    r = requests.get(
        f"{URL_BASE}?latitude={lat}&longitude={lon}&{HOURLY_PARAMS}"
    )

    return WeatherDayModel(**r.json())
