"""
Application entry point module.

This module provides the entry point for the desktop chat application.
It creates the ChatApp instance and launches the Flet application.
"""
import flet as ft

from src.app import ChatApp


def main():
    """
    Application entry point.

    Creates ChatApp instance and launches the Flet application.
    """
    app = ChatApp()
    # Explicitly set view to app for desktop window
    ft.app(target=app.main, view=ft.AppView.FLET_APP)


if __name__ == "__main__":
    main()
