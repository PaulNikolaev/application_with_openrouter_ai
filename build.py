"""
Build script module.

This module provides build functionality for creating executable files
from the Python application using PyInstaller. Supports both Windows
and Linux platforms with platform-specific build configurations.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def build_windows():
    """
    Build Windows executable file using PyInstaller.

    Installs project dependencies, creates output directory, runs PyInstaller
    with Windows-specific configuration, and moves the resulting executable
    to the bin directory.

    The build process creates a single executable file with admin privileges
    request on launch and no console window.
    """
    print("Building Windows executable...")

    # Install project dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Create output directory if it doesn't exist
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)

    # Run PyInstaller with Windows-specific configuration
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=AI Chat",
        "--clean",
        "--noupx",
        "--uac-admin",
        "src/main.py"
    ])

    # Move built executable to bin directory
    try:
        shutil.move("dist/AI Chat.exe", "bin/AIChat.exe")
        print("Windows build completed! Executable location: bin/AIChat.exe")
    except Exception:
        print("Windows build completed! Executable location: dist/AI Chat.exe")


def build_linux():
    """
    Build Linux executable file using PyInstaller.

    Installs project dependencies, creates output directory, runs PyInstaller
    with Linux-specific configuration including application icon, and moves
    the resulting executable to the bin directory.

    The build process creates a single executable file without console window.
    """
    print("Building Linux executable...")

    # Install project dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Create output directory if it doesn't exist
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)

    # Run PyInstaller with Linux-specific configuration
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=assets/icon.ico",
        "--name=aichat",
        "src/main.py"
    ])

    # Move built executable to bin directory
    try:
        shutil.move("dist/aichat", "bin/aichat")
        print("Linux build completed! Executable location: bin/aichat")
    except Exception:
        print("Linux build completed! Executable location: dist/aichat")


def main():
    """
    Main build function entry point.

    Detects the operating system platform and invokes the appropriate
    build function (Windows or Linux). Prints an error message if the
    platform is not supported.
    """
    # Detect platform and run appropriate build function
    if sys.platform.startswith('win'):
        build_windows()
    elif sys.platform.startswith('linux'):
        build_linux()
    else:
        print("Unsupported platform")


if __name__ == "__main__":
    main()
