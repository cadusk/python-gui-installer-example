"""Unit tests for the weather service."""

import pytest
from unittest.mock import Mock, patch
import requests

from services import WeatherService
from models import WeatherData, Location, WeatherErrorType, WeatherServiceError


class TestWeatherService:
    """Test cases for WeatherService class."""

    @pytest.fixture
    def service(self):
        """Create a WeatherService instance for testing."""
        return WeatherService()

    @pytest.fixture
    def mock_api_response(self):
        """Create a mock API response."""
        return {
            'current_condition': [{
                'temp_C': '20',
                'temp_F': '68',
                'FeelsLikeC': '18',
                'FeelsLikeF': '64',
                'weatherDesc': [{'value': 'Partly cloudy'}],
                'humidity': '65',
                'windspeedKmph': '15',
                'winddir16Point': 'NW',
                'pressure': '1013',
                'visibility': '10',
                'uvIndex': '5',
                'cloudcover': '50'
            }],
            'nearest_area': [{
                'areaName': [{'value': 'London'}],
                'country': [{'value': 'United Kingdom'}]
            }]
        }

    def test_get_weather_success(self, service, mock_api_response):
        """Test successful weather data retrieval."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            result = service.get_weather("London")

            assert isinstance(result, WeatherData)
            assert result.location.area_name == "London"
            assert result.location.country == "United Kingdom"
            assert result.temp_c == 20
            assert result.temp_f == 68
            assert result.condition == "Partly cloudy"
            assert result.humidity == 65

    def test_get_weather_empty_city(self, service):
        """Test error handling for empty city name."""
        with pytest.raises(WeatherServiceError) as exc_info:
            service.get_weather("")

        assert exc_info.value.error_type == WeatherErrorType.INVALID_RESPONSE
        assert "empty" in exc_info.value.message.lower()

    def test_get_weather_network_error(self, service):
        """Test error handling for network errors."""
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(WeatherServiceError) as exc_info:
                service.get_weather("London")

            assert exc_info.value.error_type == WeatherErrorType.NETWORK_ERROR
            assert "connect" in exc_info.value.message.lower()

    def test_get_weather_timeout(self, service):
        """Test error handling for timeout."""
        with patch('requests.get', side_effect=requests.exceptions.Timeout):
            with pytest.raises(WeatherServiceError) as exc_info:
                service.get_weather("London")

            assert exc_info.value.error_type == WeatherErrorType.TIMEOUT
            assert "timed out" in exc_info.value.message.lower()

    def test_get_weather_city_not_found(self, service):
        """Test error handling for city not found (404)."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            mock_get.return_value = mock_response

            with pytest.raises(WeatherServiceError) as exc_info:
                service.get_weather("InvalidCity123")

            assert exc_info.value.error_type == WeatherErrorType.CITY_NOT_FOUND
            assert "not found" in exc_info.value.message.lower()

    def test_get_weather_invalid_response(self, service):
        """Test error handling for invalid response format."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {'invalid': 'data'}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            with pytest.raises(WeatherServiceError) as exc_info:
                service.get_weather("London")

            assert exc_info.value.error_type == WeatherErrorType.INVALID_RESPONSE
            assert "invalid" in exc_info.value.message.lower()

    def test_parse_weather_data(self, service, mock_api_response):
        """Test parsing of weather data."""
        result = service._parse_weather_data(mock_api_response)

        assert isinstance(result, WeatherData)
        assert isinstance(result.location, Location)
        assert result.location.area_name == "London"
        assert result.temp_c == 20
        assert result.humidity == 65
        assert result.wind_direction == "NW"

    def test_weather_service_custom_timeout(self):
        """Test WeatherService with custom timeout."""
        service = WeatherService(timeout=5)
        assert service.timeout == 5

    def test_weather_service_custom_api_url(self):
        """Test WeatherService with custom API URL."""
        custom_url = "https://custom.api.com"
        service = WeatherService(api_url=custom_url)
        assert service.api_url == custom_url
