import sys
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 500, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Weather Finder")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Input section
        input_layout = QHBoxLayout()
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.returnPressed.connect(self.get_weather)

        self.search_button = QPushButton("Get Weather")
        self.search_button.clicked.connect(self.get_weather)

        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)
        layout.addLayout(input_layout)

        # Weather display
        self.weather_display = QTextEdit()
        self.weather_display.setReadOnly(True)
        self.weather_display.setFont(QFont("Courier", 10))
        layout.addWidget(self.weather_display)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def get_weather(self):
        city = self.city_input.text().strip()

        if not city:
            self.status_label.setText("Please enter a city name")
            self.status_label.setStyleSheet("color: red;")
            return

        self.status_label.setText(f"Fetching weather for {city}...")
        self.status_label.setStyleSheet("color: blue;")
        self.weather_display.clear()

        try:
            # Using wttr.in API - a free weather service
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract current weather information
            current = data['current_condition'][0]
            location = data['nearest_area'][0]

            weather_info = f"""
Location: {location['areaName'][0]['value']}, {location['country'][0]['value']}
Temperature: {current['temp_C']}°C ({current['temp_F']}°F)
Feels Like: {current['FeelsLikeC']}°C ({current['FeelsLikeF']}°F)
Condition: {current['weatherDesc'][0]['value']}
Humidity: {current['humidity']}%
Wind Speed: {current['windspeedKmph']} km/h
Wind Direction: {current['winddir16Point']}
Pressure: {current['pressure']} mb
Visibility: {current['visibility']} km
UV Index: {current['uvIndex']}
Cloud Cover: {current['cloudcover']}%
"""

            self.weather_display.setText(weather_info)
            self.status_label.setText("Weather data retrieved successfully!")
            self.status_label.setStyleSheet("color: green;")

        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"Error fetching weather data")
            self.status_label.setStyleSheet("color: red;")
            self.weather_display.setText(f"Network error: {str(e)}")
        except (KeyError, IndexError) as e:
            self.status_label.setText("City not found")
            self.status_label.setStyleSheet("color: red;")
            self.weather_display.setText("Unable to find weather data for this city. Please check the city name.")
        except Exception as e:
            self.status_label.setText("An error occurred")
            self.status_label.setStyleSheet("color: red;")
            self.weather_display.setText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
