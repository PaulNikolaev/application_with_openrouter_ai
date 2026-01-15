"""
Application logging utility module.

This module provides a logging system for the application with file and console
output. Logs are saved to dated files and formatted with timestamps for easy
tracking and debugging.
"""
import logging
import os
from datetime import datetime


class AppLogger:
    """
    Application logger with file and console output.

    Provides centralized logging functionality with:
    - Daily log files with date-based naming
    - Console output for real-time monitoring
    - Multiple log levels (debug, info, warning, error)
    - Formatted messages with timestamps

    Attributes:
        logs_dir (str): Directory path for log files.
        logger (logging.Logger): Configured logger instance.
    """

    def __init__(self):
        """
        Initialize logging system.

        Sets up log directory, file handler with date-based naming,
        console handler, and message formatting.
        """
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Create log file with current date: chat_app_YYYY-MM-DD.log
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"chat_app_{current_date}.log")

        # Configure log message format: YYYY-MM-DD HH:MM:SS - LEVEL - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Setup file handler with UTF-8 encoding
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Configure main logger
        self.logger = logging.getLogger('ChatApp')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """
        Log informational message.

        Used for recording important application information:
        successful operations, execution status, and state information.

        Args:
            message (str): Informational message text.
        """
        self.logger.info(message)

    def error(self, message: str, exc_info=None):
        """
        Log error message.

        Used for recording error information: exceptions, failures,
        and critical errors. Can include exception traceback.

        Args:
            message (str): Error message text.
            exc_info (bool, optional): If True, automatically includes
                exception traceback. Defaults to None.
        """
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        """
        Log debug message.

        Used for recording detailed debugging information:
        variable values, intermediate results, and execution details.

        Args:
            message (str): Debug message text.
        """
        self.logger.debug(message)

    def warning(self, message: str):
        """
        Log warning message.

        Used for recording warnings: potential issues, undesirable
        situations, and state warnings.

        Args:
            message (str): Warning message text.
        """
        self.logger.warning(message)
