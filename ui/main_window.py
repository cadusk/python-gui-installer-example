"""Main window UI for the weather application."""

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config.settings import (
    APP_NAME, APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT, APP_WINDOW_X, APP_WINDOW_Y,
    TITLE_FONT_FAMILY, TITLE_FONT_SIZE, DISPLAY_FONT_FAMILY, DISPLAY_FONT_SIZE,
    STATUS_COLOR_ERROR, STATUS_COLOR_LOADING, STATUS_COLOR_SUCCESS
)
from services import WeatherService
from models import WeatherServiceError, WeatherErrorType


class WeatherApp(QMainWindow):
    """Main application window for the weather app."""

    def __init__(self):
        """Initialize the weather application window."""
        super().__init__()
        self.weather_service = WeatherService()
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(APP_NAME)
        self.setGeometry(APP_WINDOW_X, APP_WINDOW_Y, APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Weather Finder")
        title.setFont(QFont(TITLE_FONT_FAMILY, TITLE_FONT_SIZE, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Input section
        input_layout = QHBoxLayout()
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.returnPressed.connect(self._on_search_clicked)

        self.search_button = QPushButton("Get Weather")
        self.search_button.clicked.connect(self._on_search_clicked)

        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)
        layout.addLayout(input_layout)

        # Weather display
        self.weather_display = QTextEdit()
        self.weather_display.setReadOnly(True)
        self.weather_display.setFont(QFont(DISPLAY_FONT_FAMILY, DISPLAY_FONT_SIZE))
        layout.addWidget(self.weather_display)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def _on_search_clicked(self):
        """Handle search button click or Enter key press."""
        city = self.city_input.text().strip()

        if not city:
            self._show_status("Please enter a city name", STATUS_COLOR_ERROR)
            return

        self._show_status(f"Fetching weather for {city}...", STATUS_COLOR_LOADING)
        self.weather_display.clear()

        try:
            weather_data = self.weather_service.get_weather(city)
            self.weather_display.setText(weather_data.format_display())
            self._show_status("Weather data retrieved successfully!", STATUS_COLOR_SUCCESS)

        except WeatherServiceError as e:
            self._handle_weather_error(e)

    def _handle_weather_error(self, error: WeatherServiceError):
        """Handle weather service errors and display appropriate messages.

        Args:
            error: The weather service error to handle
        """
        error_messages = {
            WeatherErrorType.NETWORK_ERROR: "Error fetching weather data",
            WeatherErrorType.CITY_NOT_FOUND: "City not found",
            WeatherErrorType.INVALID_RESPONSE: "Invalid response from weather service",
            WeatherErrorType.TIMEOUT: "Request timed out",
            WeatherErrorType.UNKNOWN: "An error occurred"
        }

        status_message = error_messages.get(error.error_type, "An error occurred")
        self._show_status(status_message, STATUS_COLOR_ERROR)
        self.weather_display.setText(error.message)

    def _show_status(self, message: str, color: str):
        """Update the status label with a message and color.

        Args:
            message: Status message to display
            color: Color for the status text
        """
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")
