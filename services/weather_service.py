"""Weather service for fetching weather data from API."""

import requests
from typing import Dict, Any

from config.settings import API_BASE_URL, API_TIMEOUT
from models import WeatherData, Location, WeatherErrorType, WeatherServiceError


class WeatherService:
    """Service for fetching and processing weather data."""

    def __init__(self, api_url: str = API_BASE_URL, timeout: int = API_TIMEOUT):
        """Initialize the weather service.

        Args:
            api_url: Base URL for the weather API
            timeout: Request timeout in seconds
        """
        self.api_url = api_url
        self.timeout = timeout

    def get_weather(self, city: str) -> WeatherData:
        """Fetch weather data for a given city.

        Args:
            city: Name of the city to fetch weather for

        Returns:
            WeatherData object containing current weather conditions

        Raises:
            WeatherServiceError: If there's an error fetching or parsing the data
        """
        if not city or not city.strip():
            raise WeatherServiceError(
                WeatherErrorType.INVALID_RESPONSE,
                "City name cannot be empty"
            )

        try:
            url = f"{self.api_url}/{city}?format=j1"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            return self._parse_weather_data(data)

        except requests.exceptions.Timeout:
            raise WeatherServiceError(
                WeatherErrorType.TIMEOUT,
                f"Request timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError:
            raise WeatherServiceError(
                WeatherErrorType.NETWORK_ERROR,
                "Failed to connect to weather service"
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise WeatherServiceError(
                    WeatherErrorType.CITY_NOT_FOUND,
                    f"City '{city}' not found"
                )
            raise WeatherServiceError(
                WeatherErrorType.NETWORK_ERROR,
                f"HTTP error: {e.response.status_code}"
            )
        except requests.exceptions.RequestException as e:
            raise WeatherServiceError(
                WeatherErrorType.NETWORK_ERROR,
                f"Network error: {str(e)}"
            )
        except (KeyError, IndexError, ValueError) as e:
            raise WeatherServiceError(
                WeatherErrorType.INVALID_RESPONSE,
                f"Invalid response format: {str(e)}"
            )
        except Exception as e:
            raise WeatherServiceError(
                WeatherErrorType.UNKNOWN,
                f"Unexpected error: {str(e)}"
            )

    def _parse_weather_data(self, data: Dict[str, Any]) -> WeatherData:
        """Parse raw API response into WeatherData object.

        Args:
            data: Raw JSON response from API

        Returns:
            WeatherData object

        Raises:
            KeyError, IndexError: If required fields are missing
        """
        current = data['current_condition'][0]
        location_data = data['nearest_area'][0]

        location = Location(
            area_name=location_data['areaName'][0]['value'],
            country=location_data['country'][0]['value']
        )

        return WeatherData(
            location=location,
            temp_c=int(current['temp_C']),
            temp_f=int(current['temp_F']),
            feels_like_c=int(current['FeelsLikeC']),
            feels_like_f=int(current['FeelsLikeF']),
            condition=current['weatherDesc'][0]['value'],
            humidity=int(current['humidity']),
            wind_speed_kmph=int(current['windspeedKmph']),
            wind_direction=current['winddir16Point'],
            pressure=int(current['pressure']),
            visibility=int(current['visibility']),
            uv_index=int(current['uvIndex']),
            cloud_cover=int(current['cloudcover'])
        )
