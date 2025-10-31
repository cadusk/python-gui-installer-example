"""Weather application entry point.

This module serves as the main entry point for the weather application.
The application has been restructured with clear separation of concerns:

- config/: Application configuration and settings
- models/: Data models and error types
- services/: Business logic for weather data fetching
- ui/: User interface components
- tests/: Unit tests for business logic

For more details, see the respective module documentation.
"""

import sys
from PyQt6.QtWidgets import QApplication

from ui import WeatherApp


def main():
    """Run the weather application."""
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
