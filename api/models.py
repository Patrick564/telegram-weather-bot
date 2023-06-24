from pydantic import BaseModel


class WeatherBase(BaseModel):
    """
    Base model for requests to open meteo API.
    """

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: int


class HourlyUnits(BaseModel):
    time: str
    temperature_2m: str
    relativehumidity_2m: str
    apparent_temperature: str
    precipitation_probability: str
    precipitation: str
    rain: str
    cloudcover: str
    uv_index: str
    is_day: str


class HourlyModel(BaseModel):
    time: list[str]
    temperature_2m: list[float]
    relativehumidity_2m: list[float]
    apparent_temperature: list[float]
    precipitation_probability: list[float]
    precipitation: list[float]
    rain: list[float]
    cloudcover: list[float]
    uv_index: list[float]
    is_day: list[float]


class WeatherDayModel(WeatherBase):
    """
    Main model for hourly weather data.
    """

    hourly_units: HourlyUnits
    hourly: HourlyModel


class DailyUnits(BaseModel):
    """
    Units type for daily weather.
    """

    time: str
    temperature_2m_max: str
    temperature_2m_min: str
    apparent_temperature_max: str
    apparent_temperature_min: str
    uv_index_max: str
    uv_index_clear_sky_max: str
    precipitation_hours: str
    precipitation_probability_max: str


class Daily(BaseModel):
    """
    Values for daily weather.
    """

    time: list[str]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]
    apparent_temperature_max: list[float]
    apparent_temperature_min: list[float]
    uv_index_max: list[float]
    uv_index_clear_sky_max: list[float]
    precipitation_hours: list[float]
    precipitation_probability_max: list[float]


class WeatherDaily(WeatherBase):
    """
    Main model for daily weather data.
    """

    daily_units: DailyUnits
    daily: Daily
