# Project Architecture Memory

## Restructuring History (2025-10-31)

### Original Problem
The project had all code in a single `weather_app.py` file (115 lines) with:
- UI code mixed with business logic
- API calls directly in the UI class
- Raw dictionaries instead of typed models
- Generic exceptions
- Hard-coded configuration values
- Untestable business logic

### Restructuring Solution Applied

#### User Preferences Selected
- **Architecture level**: Moderate structure (packages)
- **Async/Threading**: Keep synchronous (no async)
- **Improvements included**: Unit tests, data models, error enums, config file

#### New Package Structure
```
python-gui-installer-example/
├── weather_app.py              # Minimal entry point (30 lines)
├── config/
│   ├── __init__.py
│   └── settings.py             # API URLs, timeouts, UI constants
├── models/
│   ├── __init__.py
│   ├── weather.py              # WeatherData & Location dataclasses
│   └── errors.py               # WeatherErrorType enum, WeatherServiceError
├── services/
│   ├── __init__.py
│   └── weather_service.py      # All API logic & data processing
├── ui/
│   ├── __init__.py
│   └── main_window.py          # Pure PyQt6 UI, delegates to service
└── tests/
    ├── __init__.py
    ├── test_models.py          # 11 tests for data models
    └── test_weather_service.py # 9 tests for service layer
```

## Design Patterns & Practices

### 1. Separation of Concerns
- **UI layer** (ui/main_window.py): Only handles PyQt6 widgets, user interactions, display
  - Creates WeatherService instance
  - Calls service methods
  - Displays results or errors
  - NEVER contains API calls or business logic

- **Service layer** (services/weather_service.py): Pure business logic
  - Makes API requests
  - Parses JSON responses
  - Handles all error cases
  - Returns typed models
  - Independent of UI framework

- **Models** (models/): Data structures and validation
  - Dataclasses with type hints
  - Methods like `format_display()` for presentation logic
  - No external dependencies

- **Config** (config/settings.py): All constants
  - API endpoints and timeouts
  - UI dimensions and fonts
  - Status colors
  - Centralized and easy to modify

### 2. Type Safety with Dataclasses
- `Location`: area_name, country with `__str__()` method
- `WeatherData`: All weather fields as typed integers/strings
  - Includes `format_display()` method for UI presentation
  - Replaces raw dictionary access with dot notation
  - IDE autocomplete and type checking

### 3. Explicit Error Handling
- `WeatherErrorType` enum with specific error types:
  - NETWORK_ERROR
  - CITY_NOT_FOUND
  - INVALID_RESPONSE
  - TIMEOUT
  - UNKNOWN

- `WeatherServiceError` custom exception:
  - Contains error_type and message
  - Allows UI to handle different errors appropriately
  - Better error messages for users

### 4. Service Layer Pattern
- `WeatherService` class:
  - Configurable API URL and timeout (dependency injection)
  - `get_weather(city: str) -> WeatherData` public method
  - `_parse_weather_data(data: Dict) -> WeatherData` private method
  - Comprehensive error handling with specific exception types
  - Easily mockable for testing

### 5. Configuration Extraction
All magic numbers and strings moved to `config/settings.py`:
- API_BASE_URL, API_TIMEOUT
- Window dimensions and position
- Font families and sizes
- Status colors

### 6. Minimal Entry Point
`weather_app.py` reduced to ~30 lines:
- Just imports and launches the application
- Contains documentation about architecture
- Easy to understand project structure at a glance

## Testing Approach

### Test Coverage
- **20 unit tests total** (all passing in 0.08s)
- **tests/test_models.py** (11 tests):
  - Location creation and string formatting
  - WeatherData creation and display formatting
  - Error enum uniqueness
  - Custom exception behavior

- **tests/test_weather_service.py** (9 tests):
  - Successful weather fetch
  - Empty city validation
  - Network errors
  - Timeout handling
  - City not found (404)
  - Invalid response parsing
  - Data parsing logic
  - Custom configuration

### Testing Best Practices Used
- **Mocking external dependencies**: `unittest.mock.patch` for `requests.get`
- **Fixtures**: Reusable service and mock response objects
- **Comprehensive error testing**: Every error path covered
- **No UI dependencies**: All tests run without PyQt6 initialization
- **Fast execution**: < 0.1 seconds for full suite

## Benefits Achieved

### Maintainability
- Clear module boundaries with `__all__` exports
- Easy to find and modify specific functionality
- Can swap weather API without touching UI
- Configuration changes don't require code edits

### Testability
- Business logic 100% testable without UI
- Mock API responses for reliable tests
- Fast test execution enables TDD

### Extensibility
- Easy to add new features:
  - Multi-day forecast: Add to WeatherData model and service
  - Favorite cities: Add new service method
  - Different APIs: Create new service class
  - New UI views: Add to ui/ package

### Code Quality
- Type hints enable IDE support
- Explicit error types improve debugging
- Self-documenting code structure
- Reduced cognitive load (each file has single responsibility)

## Key Files Reference

### Entry Point
- **weather_app.py:21-26** - `main()` function that launches app

### Configuration
- **config/settings.py:4-5** - API_BASE_URL and API_TIMEOUT
- **config/settings.py:8-11** - Window dimensions
- **config/settings.py:19-21** - Status colors

### Models
- **models/weather.py:7-13** - Location dataclass
- **models/weather.py:16-46** - WeatherData dataclass with format_display()
- **models/errors.py:6-12** - WeatherErrorType enum
- **models/errors.py:15-26** - WeatherServiceError exception

### Business Logic
- **services/weather_service.py:23-77** - get_weather() method with error handling
- **services/weather_service.py:79-117** - _parse_weather_data() parsing logic

### UI
- **ui/main_window.py:27-30** - WeatherApp initialization with service
- **ui/main_window.py:61-74** - _on_search_clicked() delegates to service
- **ui/main_window.py:76-91** - _handle_weather_error() maps errors to UI

## Future Development Guidelines

### When Adding Features
1. **New data types** → Add to models/weather.py
2. **New API endpoints** → Extend services/weather_service.py
3. **New UI screens** → Create new file in ui/
4. **New configuration** → Add to config/settings.py
5. **Always write tests** → Add to tests/ for business logic

### Code Style to Maintain
- Use type hints everywhere
- Document all public methods with docstrings
- Keep UI methods prefixed with `_on_` or `_handle_`
- Keep service private methods prefixed with `_`
- Use explicit error types, not generic exceptions
- Configuration over hard-coded values

### Testing Requirements
- All service layer methods must have tests
- All error paths must be tested
- Use mocking for external dependencies
- Tests should be fast (< 1 second total)

## Dependencies
- **Production**: PyQt6, requests, PyInstaller
- **Development**: pytest
- **Package manager**: uv (with pyproject.toml)
- **Python version**: >=3.14

## Virtual Environment Setup
- Always use `.venv` in project root
- Activate before running: `source .venv/bin/activate`
- Install deps: `uv sync`
- Add new deps: `uv add <package>` or `uv add --dev <package>`
