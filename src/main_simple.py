"""
Simple chat application module.

This module provides a basic chat interface implementation using Flet framework
and OpenRouter API. It demonstrates a minimal working example of an AI chat application
with message display, input handling, and asynchronous API communication.
"""
import asyncio

import flet as ft

from api import OpenRouterClient
from ui import MessageBubble


class SimpleChatApp:
    """
    Simple chat application with AI integration.

    Provides a basic chat interface where users can send messages to AI models
    and receive responses. Uses OpenRouter API for AI model communication.

    Attributes:
        api_client (OpenRouterClient): Client for OpenRouter API interactions.
        chat_history (ft.Column): Container for chat message history.
        message_input (ft.TextField): Input field for user messages.
    """

    def __init__(self):
        """
        Initialize simple chat application.

        Sets up the API client for OpenRouter communication.
        """
        self.api_client = OpenRouterClient()

    def main(self, page: ft.Page):
        """
        Main application entry point.

        Configures the page layout, creates UI components, and sets up
        event handlers for the chat interface.

        Args:
            page (ft.Page): Flet page instance to configure.
        """
        # Configure page settings
        page.title = "Simple AI Chat"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = 20
        page.bgcolor = ft.Colors.GREY_900
        page.theme_mode = ft.ThemeMode.DARK

        # Create chat history container with auto-scroll
        self.chat_history = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        # Create message input field
        self.message_input = ft.TextField(
            expand=True,
            height=50,
            multiline=False,
            text_size=16,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_800,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.WHITE,
            content_padding=10,
            border_radius=8,
            hint_text="Введите сообщение здесь..."
        )

        async def send_message(e):
            """
            Handle message sending to AI model.

            Processes user input, sends it to the API, and displays the response.
            Shows loading indicator during API request.

            Args:
                e: Click event from send button.
            """
            if not self.message_input.value:
                return

            # Get message and clear input
            user_message = self.message_input.value
            self.message_input.value = ""
            page.update()

            # Add user message to chat
            self.chat_history.controls.append(
                MessageBubble(message=user_message, is_user=True)
            )

            # Show loading indicator
            loading = ft.ProgressRing()
            self.chat_history.controls.append(loading)
            page.update()

            # Send request to API asynchronously
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.api_client.send_message(
                    user_message,
                    "openai/gpt-3.5-turbo"
                )
            )

            # Remove loading indicator
            self.chat_history.controls.remove(loading)

            # Process API response
            if "error" in response:
                response_text = f"Error: {response['error']}"
            else:
                response_text = response["choices"][0]["message"]["content"]

            # Add AI response to chat
            self.chat_history.controls.append(
                MessageBubble(message=response_text, is_user=False)
            )
            page.update()

        # Create send button
        send_button = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            icon_color=ft.Colors.BLUE_400,
            on_click=send_message
        )

        # Add all components to page
        page.add(
            ft.Container(
                content=ft.Column([
                    self.chat_history,
                    ft.Row([
                        self.message_input,
                        send_button
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]),
                width=800,
                expand=True,
                padding=10,
                bgcolor=ft.Colors.GREY_800
            )
        )


if __name__ == "__main__":
    app = SimpleChatApp()
    ft.app(target=app.main)
