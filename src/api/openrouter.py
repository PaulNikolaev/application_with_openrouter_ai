"""
OpenRouter API client module.

This module provides a client for interacting with the OpenRouter API.
OpenRouter is a service that provides unified access to various language models
(GPT, Claude, etc.) through a single API interface.
"""
import os

import requests
from dotenv import load_dotenv

from src.utils.logger import AppLogger

# Load environment variables from .env file on module import
load_dotenv()


class OpenRouterClient:
    """
    Client for interacting with OpenRouter API.

    OpenRouter provides unified access to various language models (GPT, Claude, etc.)
    through a single API interface. This client handles authentication, model discovery,
    message sending, and account balance retrieval.

    Attributes:
        logger (AppLogger): Logger instance for tracking client operations.
        api_key (str): API key for authentication.
        base_url (str): Base URL for API requests.
        headers (dict): HTTP headers for API requests.
        available_models (list): List of available language models.

    Raises:
        ValueError: If API key is not found in environment variables.
    """

    def __init__(self):
        """
        Initialize OpenRouter client.

        Sets up logging, loads API credentials from environment variables,
        configures HTTP headers, and fetches available models.

        Raises:
            ValueError: If OPENROUTER_API_KEY is not found in environment variables.
        """
        self.logger = AppLogger()

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("BASE_URL")

        if not self.api_key:
            self.logger.error("OpenRouter API key not found in .env")
            raise ValueError("OpenRouter API key not found in .env")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self.logger.info("OpenRouterClient initialized successfully")

        # Fetch available models during initialization for immediate availability
        self.available_models = self.get_models()

    def get_models(self):
        """
        Retrieve list of available language models from OpenRouter API.

        Returns:
            list[dict]: List of dictionaries containing model information.
                Each dictionary has keys:
                - id (str): Model identifier for API requests
                - name (str): Human-readable model name

        Note:
            If API request fails, returns a default list of popular models
            to ensure application functionality.
        """
        self.logger.debug("Fetching available models")

        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            models_data = response.json()

            self.logger.info(f"Retrieved {len(models_data['data'])} models")

            return [
                {
                    "id": model["id"],
                    "name": model["name"]
                }
                for model in models_data["data"]
            ]
        except Exception as e:
            # Fallback to default models if API request fails
            models_default = [
                {"id": "deepseek-coder", "name": "DeepSeek"},
                {"id": "claude-3-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]
            self.logger.info(f"Retrieved {len(models_default)} models with Error: {e}")
            return models_default

    def send_message(self, message: str, model: str):
        """
        Send a message to the specified language model.

        Args:
            message (str): Text message to send to the model.
            model (str): Model identifier (e.g., "gpt-3.5-turbo", "claude-3-sonnet").

        Returns:
            dict: API response containing either:
                - Model response with generated content
                - Error information if request failed

        Note:
            The response format follows OpenRouter API specification.
            Errors are caught and returned in a consistent format.
        """
        self.logger.debug(f"Sending message to model: {model}")

        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }

        try:
            self.logger.debug("Making API request")

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data
            )

            response.raise_for_status()

            self.logger.info("Successfully received response from API")

            return response.json()

        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {"error": str(e)}

    def get_balance(self):
        """
        Retrieve current account balance from OpenRouter.

        Returns:
            str: Account balance formatted as '$X.XX' or 'Error' if request fails.

        Note:
            Balance is calculated as total credits minus total usage.
            Returns 'Error' string if API request fails or data is invalid.
        """
        try:
            response = requests.get(
                f"{self.base_url}/credits",
                headers=self.headers
            )
            data = response.json()
            if data:
                data = data.get('data')
                # Calculate available balance: total credits minus usage
                return f"${(data.get('total_credits', 0) - data.get('total_usage', 0)):.2f}"
            return "Error"
        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return "Error"
