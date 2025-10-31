"""Error types and exceptions for the weather service."""

from enum import Enum, auto


class WeatherErrorType(Enum):
    """Types of errors that can occur in the weather service."""
    NETWORK_ERROR = auto()
    CITY_NOT_FOUND = auto()
    INVALID_RESPONSE = auto()
    TIMEOUT = auto()
    UNKNOWN = auto()


class WeatherServiceError(Exception):
    """Exception raised by the weather service."""

    def __init__(self, error_type: WeatherErrorType, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.error_type.name}: {self.message}"
