"""
Login window UI component module.

This module provides a login window component for authentication,
supporting both first-time login with API key and PIN-based login.
"""
import flet as ft


class LoginWindow:
    """
    Login window component for authentication.

    Provides UI for entering API key (first-time login) or PIN code
    (subsequent logins) with buttons for login and reset functionality.

    Attributes:
        api_key_input (ft.TextField): Input field for API key.
        pin_input (ft.TextField): Input field for PIN code.
        status_text (ft.Text): Status/error message display.
        login_button (ft.ElevatedButton): Button to submit login.
        reset_button (ft.TextButton): Button to reset authentication.
    """

    def __init__(self, is_first_login: bool = True):
        """
        Initialize login window component.

        Args:
            is_first_login (bool): If True, shows API key input.
                If False, shows PIN input. Defaults to True.
        """
        self.is_first_login = is_first_login

        # Create API key input field (visible on first login)
        self.api_key_input = ft.TextField(
            label="API Key",
            hint_text="Введите ключ OpenRouter API",
            password=True,
            width=400,
            expand=False,
        )

        # Create PIN input field (visible on subsequent logins)
        self.pin_input = ft.TextField(
            label="PIN",
            hint_text="Введите 4-значный PIN",
            password=True,
            width=200,
            expand=False,
            max_length=4,
        )

        # Status/error message display
        self.status_text = ft.Text(
            value="",
            color=ft.Colors.RED_400,
            size=14,
            visible=False,
        )

        # Login button
        self.login_button = ft.ElevatedButton(
            text="Войти",
            icon=ft.icons.LOGIN,
            width=150,
        )

        # Reset button (only visible on PIN login)
        self.reset_button = ft.TextButton(
            text="Сбросить ключ",
            icon=ft.icons.RESTART_ALT,
            visible=not is_first_login,
        )

        # Create main container
        self.container = self._create_container()

    def _create_container(self) -> ft.Container:
        """
        Create main container for login window.

        Returns:
            ft.Container: Container with login form.
        """
        # Determine which input field to show
        if self.is_first_login:
            input_field = self.api_key_input
            title_text = "Первичная авторизация"
        else:
            input_field = self.pin_input
            title_text = "Вход по PIN"

        content = ft.Column(
            controls=[
                ft.Text(
                    value=title_text,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                input_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.status_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        self.login_button,
                        self.reset_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

        return ft.Container(
            content=content,
            padding=30,
            width=500,
            bgcolor=ft.Colors.GREY_900,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_700),
        )

    def show_status(self, message: str, is_error: bool = True):
        """
        Display status or error message.

        Args:
            message (str): Message to display.
            is_error (bool): If True, shows as error (red).
                If False, shows as success (green). Defaults to True.
        """
        self.status_text.value = message
        self.status_text.color = ft.Colors.RED_400 if is_error else ft.Colors.GREEN_400
        self.status_text.visible = True

    def clear_status(self):
        """Clear status message."""
        self.status_text.value = ""
        self.status_text.visible = False

    def get_api_key(self) -> str:
        """
        Get entered API key value.

        Returns:
            str: API key value or empty string.
        """
        return self.api_key_input.value or ""

    def get_pin(self) -> str:
        """
        Get entered PIN value.

        Returns:
            str: PIN value or empty string.
        """
        return self.pin_input.value or ""

    def clear_inputs(self):
        """Clear all input fields."""
        self.api_key_input.value = ""
        self.pin_input.value = ""
        self.clear_status()
