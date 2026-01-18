"""
Mobile build script module.

This module provides build functionality for creating mobile applications
(Android APK files) from the Python application using Flet build tools.
Supports Android APK building with dependency management and environment checks.
"""
import os
import sys
import subprocess
from pathlib import Path


def check_android_sdk() -> bool:
    """
    Check if Android SDK is properly configured.

    Verifies that ANDROID_HOME environment variable is set and points
    to a valid Android SDK installation directory.

    Returns:
        bool: True if Android SDK is configured, False otherwise.
    """
    android_home = os.environ.get('ANDROID_HOME')
    
    if not android_home:
        print("Error: ANDROID_HOME environment variable is not set.")
        print("Please set ANDROID_HOME to your Android SDK installation path.")
        return False
    
    if not os.path.exists(android_home):
        print(f"Error: ANDROID_HOME path does not exist: {android_home}")
        return False
    
    print(f"Android SDK found at: {android_home}")
    return True


def check_java_home() -> bool:
    """
    Check if Java Development Kit (JDK) is properly configured.

    Verifies that JAVA_HOME environment variable is set and points
    to a valid JDK installation directory.

    Returns:
        bool: True if JDK is configured, False otherwise.
    """
    java_home = os.environ.get('JAVA_HOME')
    
    if not java_home:
        print("Error: JAVA_HOME environment variable is not set.")
        print("Please set JAVA_HOME to your JDK installation path.")
        return False
    
    if not os.path.exists(java_home):
        print(f"Error: JAVA_HOME path does not exist: {java_home}")
        return False
    
    # Check if java executable exists
    java_exe = os.path.join(java_home, "bin", "java.exe" if sys.platform == "win32" else "java")
    if not os.path.exists(java_exe):
        print(f"Warning: Java executable not found at expected location: {java_exe}")
    
    print(f"JDK found at: {java_home}")
    return True


def install_mobile_dependencies() -> bool:
    """
    Install mobile-specific dependencies from requirements-mobile.txt.

    Runs pip install command to install all dependencies required for
    mobile application building.

    Returns:
        bool: True if installation succeeded, False otherwise.
    """
    requirements_file = Path("requirements-mobile.txt")
    
    if not requirements_file.exists():
        print(f"Error: {requirements_file} not found.")
        return False
    
    print("Installing mobile dependencies...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print("Mobile dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing mobile dependencies: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def build_android_apk(
    project_name: str = "AIChat",
    package_name: str = "com.example.aichat",
    org: str = None,
    version: str = "1.0.0",
    build_number: int = 1,
    android_min_sdk: int = 21,
    icon_path: str = None,
    android_permissions: list = None
) -> bool:
    """
    Build Android APK file using Flet build tools.

    Performs environment checks, installs dependencies, and executes
    flet build apk command with specified parameters. The resulting
    APK file will be located at:
    build/android/app/build/outputs/apk/release/app-release.apk

    Args:
        project_name (str): Name of the project/application. Defaults to "AIChat".
        package_name (str): Android package name (e.g., com.example.app).
            Defaults to "com.example.aichat".
        org (str, optional): Organization identifier (e.g., com.example).
            If None, derived from package_name. Defaults to None.
        version (str): Application version string. Defaults to "1.0.0".
        build_number (int): Build number. Defaults to 1.
        android_min_sdk (int): Minimum Android SDK version. Defaults to 21 (Android 5.0).
        icon_path (str, optional): Path to application icon (PNG format).
            If None, uses default icon. Defaults to None.
        android_permissions (list, optional): List of Android permissions to request.
            Defaults to ["INTERNET", "ACCESS_NETWORK_STATE", "WRITE_EXTERNAL_STORAGE"].

    Returns:
        bool: True if build succeeded, False otherwise.
    """
    print("=" * 60)
    print("Building Android APK")
    print("=" * 60)
    print()
    
    # Check environment prerequisites
    print("Checking prerequisites...")
    if not check_android_sdk():
        return False
    
    if not check_java_home():
        return False
    
    print()
    
    # Install mobile dependencies
    if not install_mobile_dependencies():
        return False
    
    print()
    
    # Set default Android permissions if not provided
    if android_permissions is None:
        android_permissions = [
            "INTERNET",
            "ACCESS_NETWORK_STATE",
            "WRITE_EXTERNAL_STORAGE"
        ]
    
    # Derive organization from package_name if not provided
    if org is None:
        # Extract org from package_name (e.g., "com.example" from "com.example.aichat")
        parts = package_name.split('.')
        if len(parts) >= 2:
            org = '.'.join(parts[:-1])
        else:
            org = "com.example"
    
    # Prepare flet build command
    print("Preparing Flet build command...")
    build_command = [
        "flet",
        "build",
        "apk",
        "--project-name", project_name,
        "--package-name", package_name,
        "--org", org,
        "--version", version,
        "--build-number", str(build_number),
        "--android-min-sdk", str(android_min_sdk),
    ]
    
    # Add icon if provided and exists
    if icon_path:
        icon_file = Path(icon_path)
        if icon_file.exists():
            build_command.extend(["--icon", str(icon_file)])
            print(f"Using icon: {icon_path}")
        else:
            print(f"Warning: Icon file not found: {icon_path}")
    
    # Add Android permissions
    if android_permissions:
        permissions_str = ",".join(android_permissions)
        build_command.extend(["--android-permissions", permissions_str])
        print(f"Android permissions: {', '.join(android_permissions)}")
    
    print()
    print("Starting APK build process...")
    print(f"Project: {project_name}")
    print(f"Package: {package_name}")
    print(f"Organization: {org}")
    print(f"Version: {version} (build {build_number})")
    print(f"Min SDK: {android_min_sdk}")
    if android_permissions:
        print(f"Permissions: {', '.join(android_permissions)}")
    print()
    
    # Execute build command
    try:
        result = subprocess.run(
            build_command,
            check=True,
            text=True
        )
        
        print()
        print("=" * 60)
        print("APK build completed successfully!")
        print("=" * 60)
        apk_path = Path("build/android/app/build/outputs/apk/release/app-release.apk")
        if apk_path.exists():
            print(f"APK location: {apk_path.absolute()}")
        else:
            print("APK location: build/android/app/build/outputs/apk/release/app-release.apk")
        print("=" * 60)
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("APK build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("Error: 'flet' command not found.")
        print("=" * 60)
        print("Please ensure Flet is installed and available in PATH.")
        print("Try running: pip install flet-builder")
        return False


def main():
    """
    Main build function entry point.

    Executes Android APK build with default parameters.
    Automatically checks for icon.png in assets directory.
    Can be customized by modifying function parameters.
    """
    # Check for PNG icon in assets directory
    icon_path = None
    icon_png = Path("assets/icon.png")
    icon_ico = Path("assets/icon.ico")
    
    if icon_png.exists():
        icon_path = str(icon_png)
        print(f"Found icon: {icon_path}")
    elif icon_ico.exists():
        print("Note: Found icon.ico but Android requires PNG format.")
        print("      APK will use default Flet icon. To use custom icon:")
        print("      Convert icon.ico to PNG (1024x1024 recommended) and save as assets/icon.png")
    else:
        print("Note: No icon found. APK will use default Flet icon.")
    
    # Default build parameters
    success = build_android_apk(
        project_name="AIChat",
        package_name="com.example.aichat",
        version="1.0.0",
        build_number=1,
        android_min_sdk=21,
        icon_path=icon_path  # Will be None if PNG not found, uses default Flet icon
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
