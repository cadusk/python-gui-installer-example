# Building Weather App Installers

This document explains how to build installer packages for Weather App on macOS, Windows, and Linux.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Building Locally](#building-locally)
- [GitHub Actions (CI/CD)](#github-actions-cicd)
- [Platform-Specific Details](#platform-specific-details)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### All Platforms

- Python 3.10 or higher
- Virtual environment (recommended)
- All dependencies from `requirements.txt`

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Platform-Specific Requirements

**macOS:**
- Xcode Command Line Tools: `xcode-select --install`
- `hdiutil` (included with macOS) for DMG creation

**Windows:**
- [NSIS](https://nsis.sourceforge.io/) (optional, for creating installers)
  ```powershell
  choco install nsis -y
  ```

**Linux:**
- Standard build tools
- Optional: `fpm` for creating .deb/.rpm packages
- Optional: `appimagetool` for creating AppImages

## Quick Start

### Using the Build Script

The easiest way to build is using the provided `build.py` script:

```bash
# Activate virtual environment
source .venv/bin/activate

# Build for current platform
python build.py

# Clean build artifacts
python build.py --clean
```

### Manual Build

You can also build manually using PyInstaller:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run PyInstaller with the spec file
python -m PyInstaller --clean --noconfirm weather_app.spec
```

Build output will be in:
- `dist/` - Final executables and packages
- `build/` - Temporary build files (can be deleted)

## Building Locally

### macOS

The build script creates a `.app` bundle and a DMG installer:

```bash
python build.py
```

Output:
- `dist/WeatherApp.app` - macOS application bundle
- `dist/WeatherApp-1.0.0-macOS.dmg` - DMG installer

**Manual DMG creation:**
```bash
hdiutil create -volname WeatherApp -srcfolder dist/WeatherApp.app \
  -ov -format UDZO dist/WeatherApp-macOS.dmg
```

**Code Signing (for distribution):**
```bash
# Sign the app
codesign --force --deep --sign "Developer ID Application: Your Name" \
  dist/WeatherApp.app

# Verify signature
codesign --verify --verbose dist/WeatherApp.app

# Notarize (for macOS 10.15+)
xcrun notarytool submit dist/WeatherApp-1.0.0-macOS.dmg \
  --apple-id your@email.com --team-id TEAMID --password app-specific-password
```

### Windows

The build script creates an executable and optionally an installer:

```bash
python build.py
```

Output:
- `dist/WeatherApp/` - Application directory
- `dist/WeatherApp-1.0.0-Windows-Setup.exe` - Installer (if NSIS is installed)

**Without NSIS:**
The executable will be in `dist/WeatherApp/WeatherApp.exe` and can be distributed as-is.

**With NSIS:**
Install NSIS and the build script will automatically create an installer.

**Code Signing (optional):**
```powershell
# Using SignTool (requires certificate)
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com \
  /td sha256 /fd sha256 dist/WeatherApp/WeatherApp.exe
```

### Linux

The build script creates a standalone binary:

```bash
python build.py
```

Output:
- `dist/WeatherApp/` - Application directory with executable

**Creating a .deb package:**
```bash
# Install fpm
gem install fpm

# Create package
fpm -s dir -t deb -n weatherapp -v 1.0.0 \
  --prefix /opt/weatherapp dist/WeatherApp
```

**Creating an AppImage:**
```bash
# Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p WeatherApp.AppDir/usr/bin
cp -r dist/WeatherApp/* WeatherApp.AppDir/usr/bin/
cp icons/icon.png WeatherApp.AppDir/weatherapp.png

# Create desktop entry
cat > WeatherApp.AppDir/weatherapp.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Weather App
Icon=weatherapp
Exec=WeatherApp
Categories=Utility;
EOF

# Build AppImage
./appimagetool-x86_64.AppImage WeatherApp.AppDir WeatherApp-1.0.0-Linux.AppImage
```

## GitHub Actions (CI/CD)

The repository includes a GitHub Actions workflow that automatically builds installers for all platforms.

### Automatic Builds

The workflow triggers on:
- Push to `main` branch
- Pull requests
- Tags starting with `v*` (e.g., `v1.0.0`)
- Manual workflow dispatch

### Workflow Jobs

1. **Build Job**: Runs in parallel on Ubuntu, Windows, and macOS runners
   - Installs dependencies
   - Runs PyInstaller
   - Creates platform-specific installers
   - Uploads build artifacts

2. **Release Job**: Only runs on version tags
   - Downloads all artifacts
   - Creates a GitHub Release
   - Attaches installers to the release

### Creating a Release

To create a new release with installers:

```bash
# Tag a release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Build installers for all platforms
# 2. Create a GitHub Release
# 3. Upload installers as release assets
```

### Downloading Artifacts

For builds on non-tag commits, artifacts are available for 30 days:

1. Go to the "Actions" tab in GitHub
2. Click on the workflow run
3. Download artifacts from the "Artifacts" section

## Platform-Specific Details

### Application Structure

**macOS (.app bundle):**
```
WeatherApp.app/
├── Contents/
│   ├── Info.plist
│   ├── MacOS/
│   │   └── WeatherApp (executable)
│   └── Resources/
│       └── icon.icns
```

**Windows (folder):**
```
WeatherApp/
├── WeatherApp.exe (executable)
├── Qt6*.dll
├── Python*.dll
└── [other dependencies]
```

**Linux (folder):**
```
WeatherApp/
├── WeatherApp (executable)
├── Qt6*.so
└── [other dependencies]
```

### Executable Size

Expected sizes (approximate):
- macOS: 100-150 MB (app bundle)
- Windows: 80-120 MB (folder)
- Linux: 90-130 MB (folder)

These sizes include:
- Python interpreter
- PyQt6 framework
- SSL libraries
- Application code

### Icon Files

Icons are stored in `icons/`:
- `icon.png` - Source icon (512x512)
- `icon.ico` - Windows icon (multi-size)
- `icon.icns` - macOS icon
- `generate_icons.py` - Script to regenerate icons

To regenerate icons:
```bash
python icons/generate_icons.py
```

## Troubleshooting

### Common Issues

**Issue: "PyInstaller not found"**
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install pyinstaller
```

**Issue: "Module not found" errors at runtime**
```python
# Add missing modules to weather_app.spec hiddenimports:
hiddenimports = [
    'PyQt6.QtCore',
    'missing_module_name',
]
```

**Issue: SSL certificate errors**
- The spec file includes `certifi` data files
- Verify with: `python -c "import certifi; print(certifi.where())"`

**Issue: Antivirus flags the executable**
- This is common with PyInstaller executables
- Solution: Code sign the executable
- Or: Submit to antivirus vendors for whitelisting

**Issue: "Application damaged" on macOS**
```bash
# Remove quarantine attribute
xattr -cr dist/WeatherApp.app
```

**Issue: Large executable size**
- PyQt6 includes many modules
- Consider using `--exclude-module` for unused Qt modules
- UPX compression is already enabled in the spec file

### Debug Build

For debugging issues, create a debug build:

```bash
# Edit weather_app.spec and set:
# debug=True, console=True

python -m PyInstaller --clean --noconfirm weather_app.spec

# Run and check console output
./dist/WeatherApp/WeatherApp  # Linux/macOS
dist\WeatherApp\WeatherApp.exe  # Windows
```

### Logging

Enable PyInstaller logging:
```bash
python -m PyInstaller --log-level DEBUG --clean weather_app.spec
```

## Build Best Practices

1. **Always build on the target platform** - PyInstaller creates platform-specific executables
2. **Test on clean systems** - Use VMs to verify no system dependencies
3. **Version consistently** - Update version in `build.py` and `weather_app.spec`
4. **Code sign** - Sign executables for distribution (especially macOS and Windows)
5. **Clean before release builds** - Run `python build.py --clean` first
6. **Document changes** - Update this file when changing the build process

## Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [NSIS Documentation](https://nsis.sourceforge.io/Docs/)
- [macOS Code Signing](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

For build issues:
1. Check this documentation
2. Review PyInstaller logs
3. Test with a debug build
4. Check GitHub Issues for similar problems
