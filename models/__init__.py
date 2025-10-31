"""Data models for the weather application."""

from .weather import WeatherData, Location
from .errors import WeatherErrorType, WeatherServiceError

__all__ = ["WeatherData", "Location", "WeatherErrorType", "WeatherServiceError"]
