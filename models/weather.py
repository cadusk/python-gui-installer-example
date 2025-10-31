"""Weather data models."""

from dataclasses import dataclass


@dataclass
class Location:
    """Represents a geographic location."""
    area_name: str
    country: str

    def __str__(self) -> str:
        return f"{self.area_name}, {self.country}"


@dataclass
class WeatherData:
    """Represents current weather conditions."""
    location: Location
    temp_c: int
    temp_f: int
    feels_like_c: int
    feels_like_f: int
    condition: str
    humidity: int
    wind_speed_kmph: int
    wind_direction: str
    pressure: int
    visibility: int
    uv_index: int
    cloud_cover: int

    def format_display(self) -> str:
        """Format weather data for display."""
        return f"""
Location: {self.location}
Temperature: {self.temp_c}°C ({self.temp_f}°F)
Feels Like: {self.feels_like_c}°C ({self.feels_like_f}°F)
Condition: {self.condition}
Humidity: {self.humidity}%
Wind Speed: {self.wind_speed_kmph} km/h
Wind Direction: {self.wind_direction}
Pressure: {self.pressure} mb
Visibility: {self.visibility} km
UV Index: {self.uv_index}
Cloud Cover: {self.cloud_cover}%
"""
