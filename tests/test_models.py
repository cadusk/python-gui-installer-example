"""Unit tests for data models."""

import pytest

from models import WeatherData, Location, WeatherErrorType, WeatherServiceError


class TestLocation:
    """Test cases for Location model."""

    def test_location_creation(self):
        """Test Location object creation."""
        location = Location(area_name="London", country="United Kingdom")

        assert location.area_name == "London"
        assert location.country == "United Kingdom"

    def test_location_str(self):
        """Test Location string representation."""
        location = Location(area_name="Paris", country="France")

        assert str(location) == "Paris, France"


class TestWeatherData:
    """Test cases for WeatherData model."""

    @pytest.fixture
    def sample_weather(self):
        """Create a sample WeatherData object."""
        location = Location(area_name="Tokyo", country="Japan")
        return WeatherData(
            location=location,
            temp_c=25,
            temp_f=77,
            feels_like_c=23,
            feels_like_f=73,
            condition="Sunny",
            humidity=60,
            wind_speed_kmph=10,
            wind_direction="E",
            pressure=1015,
            visibility=10,
            uv_index=7,
            cloud_cover=20
        )

    def test_weather_data_creation(self, sample_weather):
        """Test WeatherData object creation."""
        assert sample_weather.location.area_name == "Tokyo"
        assert sample_weather.temp_c == 25
        assert sample_weather.condition == "Sunny"
        assert sample_weather.humidity == 60

    def test_weather_data_format_display(self, sample_weather):
        """Test weather data formatting for display."""
        display = sample_weather.format_display()

        assert "Tokyo, Japan" in display
        assert "25°C" in display
        assert "77°F" in display
        assert "Sunny" in display
        assert "60%" in display
        assert "10 km/h" in display
        assert "E" in display

    def test_weather_data_all_fields(self, sample_weather):
        """Test that all WeatherData fields are accessible."""
        assert sample_weather.temp_c == 25
        assert sample_weather.temp_f == 77
        assert sample_weather.feels_like_c == 23
        assert sample_weather.feels_like_f == 73
        assert sample_weather.condition == "Sunny"
        assert sample_weather.humidity == 60
        assert sample_weather.wind_speed_kmph == 10
        assert sample_weather.wind_direction == "E"
        assert sample_weather.pressure == 1015
        assert sample_weather.visibility == 10
        assert sample_weather.uv_index == 7
        assert sample_weather.cloud_cover == 20


class TestWeatherErrorType:
    """Test cases for WeatherErrorType enum."""

    def test_error_types_exist(self):
        """Test that all error types are defined."""
        assert WeatherErrorType.NETWORK_ERROR
        assert WeatherErrorType.CITY_NOT_FOUND
        assert WeatherErrorType.INVALID_RESPONSE
        assert WeatherErrorType.TIMEOUT
        assert WeatherErrorType.UNKNOWN

    def test_error_types_are_unique(self):
        """Test that error types have unique values."""
        error_values = [e.value for e in WeatherErrorType]
        assert len(error_values) == len(set(error_values))


class TestWeatherServiceError:
    """Test cases for WeatherServiceError exception."""

    def test_error_creation(self):
        """Test WeatherServiceError creation."""
        error = WeatherServiceError(
            WeatherErrorType.NETWORK_ERROR,
            "Connection failed"
        )

        assert error.error_type == WeatherErrorType.NETWORK_ERROR
        assert error.message == "Connection failed"

    def test_error_str(self):
        """Test WeatherServiceError string representation."""
        error = WeatherServiceError(
            WeatherErrorType.CITY_NOT_FOUND,
            "City 'InvalidCity' not found"
        )

        error_str = str(error)
        assert "CITY_NOT_FOUND" in error_str
        assert "InvalidCity" in error_str

    def test_error_is_exception(self):
        """Test that WeatherServiceError is an Exception."""
        error = WeatherServiceError(
            WeatherErrorType.TIMEOUT,
            "Request timed out"
        )

        assert isinstance(error, Exception)

    def test_error_can_be_raised(self):
        """Test that WeatherServiceError can be raised and caught."""
        with pytest.raises(WeatherServiceError) as exc_info:
            raise WeatherServiceError(
                WeatherErrorType.UNKNOWN,
                "Unknown error occurred"
            )

        assert exc_info.value.error_type == WeatherErrorType.UNKNOWN
        assert "Unknown error" in exc_info.value.message
