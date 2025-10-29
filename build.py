#!/usr/bin/env python3
"""
Build script for Weather App - Creates installers for macOS, Windows, and Linux.

Usage:
    python build.py              # Build for current platform
    python build.py --clean      # Clean build directories
    python build.py --help       # Show help
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DIST_DIR = PROJECT_ROOT / 'dist'
BUILD_DIR = PROJECT_ROOT / 'build'
SPEC_FILE = PROJECT_ROOT / 'weather_app.spec'

# Platform detection
SYSTEM = platform.system()
IS_MACOS = SYSTEM == 'Darwin'
IS_WINDOWS = SYSTEM == 'Windows'
IS_LINUX = SYSTEM == 'Linux'

# Build configuration
APP_NAME = 'WeatherApp'
VERSION = '1.0.0'


def print_header(message):
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {message}")
    print(f"{'=' * 70}\n")


def clean_build():
    """Remove build and dist directories."""
    print_header("Cleaning build directories")

    dirs_to_clean = [BUILD_DIR, DIST_DIR]
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            print(f"Removing: {dir_path}")
            shutil.rmtree(dir_path)
        else:
            print(f"Already clean: {dir_path}")

    print("\nClean complete!")


def run_command(cmd, description):
    """Run a shell command with error handling."""
    print(f"\n>>> {description}")
    print(f"    Command: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,
            text=True,
            cwd=PROJECT_ROOT
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError: {description} failed!")
        print(f"Exit code: {e.returncode}")
        return False


def build_with_pyinstaller():
    """Run PyInstaller to create the executable."""
    print_header(f"Building {APP_NAME} with PyInstaller")

    if not SPEC_FILE.exists():
        print(f"Error: Spec file not found: {SPEC_FILE}")
        return False

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        str(SPEC_FILE)
    ]

    return run_command(cmd, "Running PyInstaller")


def create_macos_dmg():
    """Create a DMG installer for macOS."""
    print_header("Creating macOS DMG installer")

    app_bundle = DIST_DIR / f'{APP_NAME}.app'
    if not app_bundle.exists():
        print(f"Error: App bundle not found: {app_bundle}")
        return False

    dmg_name = f'{APP_NAME}-{VERSION}-macOS.dmg'
    dmg_path = DIST_DIR / dmg_name

    # Remove existing DMG if present
    if dmg_path.exists():
        dmg_path.unlink()

    # Create DMG using hdiutil
    cmd = [
        'hdiutil', 'create',
        '-volname', APP_NAME,
        '-srcfolder', str(app_bundle),
        '-ov',
        '-format', 'UDZO',
        str(dmg_path)
    ]

    if run_command(cmd, "Creating DMG"):
        print(f"\n✓ DMG created: {dmg_path}")
        return True
    return False


def create_windows_installer():
    """Create a Windows installer using NSIS."""
    print_header("Creating Windows installer")

    # Check if NSIS is installed
    try:
        subprocess.run(['makensis', '-VERSION'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: NSIS not found. Install NSIS to create installer.")
        print("Skipping installer creation.")
        print(f"Executable available at: {DIST_DIR / APP_NAME}")
        return True

    # Create NSIS script
    nsis_script = create_nsis_script()
    nsis_file = PROJECT_ROOT / 'installer.nsi'

    with open(nsis_file, 'w') as f:
        f.write(nsis_script)

    cmd = ['makensis', str(nsis_file)]
    success = run_command(cmd, "Running NSIS")

    # Clean up NSIS script
    if nsis_file.exists():
        nsis_file.unlink()

    return success


def create_nsis_script():
    """Generate NSIS installer script."""
    return f'''
!define APP_NAME "{APP_NAME}"
!define APP_VERSION "{VERSION}"
!define PUBLISHER "Weather App"
!define DIST_DIR "dist\\{APP_NAME}"

Name "${{APP_NAME}}"
OutFile "dist\\${{APP_NAME}}-${{APP_VERSION}}-Windows-Setup.exe"
InstallDir "$PROGRAMFILES64\\${{APP_NAME}}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "${{DIST_DIR}}\\*.*"

    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\{APP_NAME}.exe"
    CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\{APP_NAME}.exe"

    WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\Uninstall.exe"
    RMDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
    RMDir "$SMPROGRAMS\\${{APP_NAME}}"
SectionEnd
'''


def create_linux_package():
    """Create a Linux package or AppImage."""
    print_header("Creating Linux package")

    app_dir = DIST_DIR / APP_NAME
    if not app_dir.exists():
        print(f"Error: Application directory not found: {app_dir}")
        return False

    print(f"Linux binary available at: {app_dir}")
    print("\nTo create a .deb package, install 'fpm':")
    print("  gem install fpm")
    print(f"  fpm -s dir -t deb -n {APP_NAME.lower()} -v {VERSION} {app_dir}")
    print("\nTo create an AppImage, use 'appimagetool':")
    print("  https://appimage.github.io/appimagetool/")

    return True


def build():
    """Main build function."""
    print_header(f"Building {APP_NAME} v{VERSION} for {SYSTEM}")

    # Step 1: Build with PyInstaller
    if not build_with_pyinstaller():
        print("\n❌ Build failed!")
        return False

    # Step 2: Create platform-specific installer
    if IS_MACOS:
        success = create_macos_dmg()
    elif IS_WINDOWS:
        success = create_windows_installer()
    elif IS_LINUX:
        success = create_linux_package()
    else:
        print(f"Warning: Unknown platform: {SYSTEM}")
        success = True

    if success:
        print_header("Build Complete!")
        print(f"✓ Build artifacts are in: {DIST_DIR}")

        # List output files
        if DIST_DIR.exists():
            print("\nOutput files:")
            for item in DIST_DIR.iterdir():
                size = item.stat().st_size if item.is_file() else '-'
                size_mb = f"{size / (1024*1024):.1f} MB" if size != '-' else 'DIR'
                print(f"  - {item.name} ({size_mb})")
    else:
        print("\n❌ Installer creation failed (build artifacts may still be usable)")

    return success


def main():
    """Parse arguments and run build."""
    parser = argparse.ArgumentParser(
        description=f'Build {APP_NAME} for distribution',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py              Build for current platform
  python build.py --clean      Remove build artifacts
  python build.py --help       Show this help message
        """
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean build directories and exit'
    )

    args = parser.parse_args()

    if args.clean:
        clean_build()
        return 0

    # Ensure we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    ):
        print("Warning: Not running in a virtual environment!")
        print("It's recommended to activate .venv first:")
        print("  source .venv/bin/activate  # macOS/Linux")
        print("  .venv\\Scripts\\activate     # Windows")
        response = input("\nContinue anyway? [y/N]: ")
        if response.lower() != 'y':
            return 1

    success = build()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
