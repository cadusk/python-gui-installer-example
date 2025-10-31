# Weather App

A modern, cross-platform desktop weather application built with Python and PyQt6. Get real-time weather information for any city worldwide with a clean, intuitive interface.

## Features

- **Real-time Weather Data**: Fetches current weather conditions from wttr.in API
- **Comprehensive Information**: Displays temperature, humidity, wind speed, pressure, visibility, UV index, and more
- **Dual Temperature Units**: Shows both Celsius and Fahrenheit
- **Clean UI**: Modern PyQt6 interface with intuitive design
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Standalone Builds**: Distributable executables for easy installation
- **No API Key Required**: Uses the free wttr.in weather service
- **Error Handling**: Robust error handling with user-friendly messages
- **Keyboard Support**: Press Enter to search for weather

## Prerequisites

- Python 3.14 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver

## Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-gui-installer-example
   ```

2. **Install uv** (if not already installed)
   ```bash
   pip install uv
   ```

3. **Install dependencies**
   ```bash
   # uv will automatically create .venv and install all dependencies
   uv sync
   ```

4. **Run the application**
   ```bash
   uv run python weather_app.py
   ```

### Alternative: Using Standalone Executables

Pre-built executables are available in the [Releases](../../releases) section for:
- Windows (`.exe`)
- macOS (`.dmg`)
- Linux (standalone binary)

Simply download and run - no Python installation required!

## Usage

1. Launch the application
2. Enter a city name in the input field
3. Click "Get Weather" or press Enter
4. View the current weather conditions for that location

### Example Queries

- `London`
- `New York`
- `Tokyo`
- `Paris, France`

## Development

### Project Structure

```
python-gui-installer-example/
├── weather_app.py          # Main entry point
├── config/                 # Application configuration
│   └── settings.py         # Settings and constants
├── models/                 # Data models
│   ├── weather.py          # Weather data structures
│   └── errors.py           # Error types and exceptions
├── services/               # Business logic
│   └── weather_service.py  # Weather API integration
├── ui/                     # User interface
│   └── main_window.py      # Main window UI components
├── tests/                  # Unit tests
├── icons/                  # Application icons
├── build.py                # Build script for creating executables
├── weather_app.spec        # PyInstaller specification
├── pyproject.toml          # Project dependencies
└── BUILDING.md             # Detailed build instructions
```

### Architecture

The application follows a clean architecture with separation of concerns:

- **UI Layer** (`ui/`): PyQt6-based graphical interface
- **Service Layer** (`services/`): Business logic and API integration
- **Model Layer** (`models/`): Data structures and domain models
- **Config Layer** (`config/`): Application settings and constants

### API Integration

The application uses the [wttr.in](https://wttr.in) API:
- **Endpoint**: `https://wttr.in/{city}?format=j1`
- **Format**: JSON
- **Authentication**: None required
- **Rate Limiting**: Reasonable use policy
- **Timeout**: 10 seconds

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=services --cov=models

# Run specific test file
uv run pytest tests/test_weather_service.py
```

### Development Setup

```bash
# Install all dependencies including dev dependencies
uv sync

# Format code (if using formatters)
uv run black .

# Lint code (if using linters)
uv run flake8 .
```

### Configuration

Application settings can be customized in `config/settings.py`:

- **API_BASE_URL**: Weather API endpoint
- **API_TIMEOUT**: Request timeout (seconds)
- **APP_NAME**: Application window title
- **Window dimensions**: Width, height, position
- **Font settings**: Font families and sizes
- **Status colors**: UI color scheme

## Building Executables

### Quick Build

```bash
# Build for current platform
uv run python build.py

# Clean previous build artifacts
uv run python build.py --clean
```

### Platform-Specific Builds

The application can be built into standalone executables for distribution:

- **macOS**: `.app` bundle and `.dmg` installer
- **Windows**: `.exe` executable and optional NSIS installer
- **Linux**: Standalone binary, `.deb`, `.rpm`, or AppImage

For detailed build instructions, see [BUILDING.md](BUILDING.md).

### Automated Builds (CI/CD)

GitHub Actions automatically builds executables for all platforms:
- Triggered on pushes to `main`, pull requests, or version tags
- Artifacts available for 30 days
- Releases created automatically for version tags (e.g., `v1.0.0`)

## Dependencies

### Core Dependencies
- **PyQt6** (>=6.10.0): GUI framework
- **requests** (>=2.32.5): HTTP client for API calls
- **PyInstaller** (>=6.16.0): Executable builder

### Development Dependencies
- **pytest** (>=8.4.2): Testing framework
- **Pillow** (>=11.0.0): Icon generation

All dependencies are managed via `pyproject.toml` and installed automatically with `uv sync`.

## Error Handling

The application includes robust error handling for:

- **Network Errors**: Connection issues, timeouts
- **City Not Found**: Invalid or unknown city names
- **Invalid Response**: Malformed API responses
- **Timeout**: Requests exceeding timeout limit
- **Unknown Errors**: Unexpected failures

All errors are displayed with user-friendly messages and appropriate status indicators.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Run tests**: `uv run pytest`
5. **Commit your changes**: `git commit -m "Description"`
6. **Push to your fork**: `git push origin feature-name`
7. **Create a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described
- Ensure all tests pass before submitting PR

## License

<!-- Add your license here -->
[Specify your license - e.g., MIT, GPL, Apache 2.0]

## Acknowledgments

- Weather data provided by [wttr.in](https://wttr.in)
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Package management with [uv](https://docs.astral.sh/uv/)
- Icons generated using Pillow

## Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Build Problems**: See [BUILDING.md](BUILDING.md)

## Roadmap

Potential future enhancements:
- [ ] Multi-day weather forecast
- [ ] Weather alerts and notifications
- [ ] Multiple location favorites
- [ ] Weather history and trends
- [ ] Dark mode support
- [ ] Customizable units (metric/imperial)
- [ ] System tray integration
- [ ] Weather maps and radar

---

**Note**: This is an educational example project demonstrating how to create a cross-platform Python GUI application with proper packaging and distribution.
