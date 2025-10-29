# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Environment Setup

- Python's virtual environment should always be installed on `.venv` on the project's root folder.
- Always ensure you're in a python's virtualenv before installing packages or trying to run tests or the application itself.

## Project Overview

This is a PyQt6-based weather application that provides a GUI for fetching current weather information for any city using the wttr.in API (free, no API key required).

## Development Setup

### Initial Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Ensure you're in the virtual environment first
source .venv/bin/activate

# Run the application
python weather_app.py
```

## Architecture

### Main Components

- **WeatherApp (QMainWindow)**: The main application window containing all UI components
  - City input field with Enter key support
  - Search button triggering weather fetch
  - Read-only text display for weather information
  - Status label for user feedback with color-coded messages

- **API Integration**: Uses wttr.in REST API
  - Endpoint: `https://wttr.in/{city}?format=j1`
  - Returns JSON with current conditions and location data
  - No authentication required
  - 10-second timeout on requests

### Data Flow

1. User enters city name → triggers `get_weather()` method
2. HTTP request sent to wttr.in API with city parameter
3. JSON response parsed for current conditions and location
4. Weather data formatted and displayed in the text area
5. Status updates shown with appropriate color coding (blue=loading, green=success, red=error)