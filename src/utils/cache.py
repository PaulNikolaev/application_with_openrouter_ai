"""
Chat cache utility module.

This module provides SQLite-based caching for chat history and analytics data.
It ensures thread-safe database operations and provides methods for storing,
retrieving, and managing chat messages and analytics records.
"""
import sqlite3
import threading
from datetime import datetime


class ChatCache:
    """
    Thread-safe chat history cache using SQLite database.

    Provides persistent storage for chat messages with metadata including
    model information, timestamps, and token usage. Supports analytics
    data storage and formatted history retrieval.

    Attributes:
        db_name (str): SQLite database file name.
        local (threading.local): Thread-local storage for database connections.
    """

    def __init__(self):
        """
        Initialize chat cache system.

        Creates SQLite database file, sets up thread-local connection storage,
        and creates necessary database tables.
        """
        self.db_name = 'chat_cache.db'

        # Thread-local storage ensures each thread has its own connection
        self.local = threading.local()

        self.create_tables()

    def get_connection(self):
        """
        Get database connection for current thread.

        Returns a thread-local database connection, creating one if it doesn't
        exist. This ensures thread-safe database operations.

        Returns:
            sqlite3.Connection: Database connection object for current thread.
        """
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_name)
        return self.local.connection

    def create_tables(self):
        """
        Create necessary database tables.

        Creates two tables:
        - messages: stores chat messages with metadata
        - analytics_messages: stores analytics data for performance tracking
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                user_message TEXT,
                ai_response TEXT,
                timestamp DATETIME,
                tokens_used INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                model TEXT,
                message_length INTEGER,
                response_time FLOAT,
                tokens_used INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    def save_message(self, model, user_message, ai_response, tokens_used):
        """
        Save new chat message to database.

        Args:
            model (str): Model identifier used for the message.
            user_message (str): User's message text.
            ai_response (str): AI model's response text.
            tokens_used (int): Number of tokens consumed.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO messages (model, user_message, ai_response, timestamp, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (model, user_message, ai_response, datetime.now(), tokens_used))
        conn.commit()

    def get_chat_history(self, limit=50):
        """
        Retrieve recent chat messages from database.

        Args:
            limit (int, optional): Maximum number of messages to return.
                Defaults to 50.

        Returns:
            list: List of tuples containing message data, sorted by timestamp
                in descending order (newest first).
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    def save_analytics(self, timestamp, model, message_length, response_time, tokens_used):
        """
        Save analytics data to database.

        Args:
            timestamp (datetime): Timestamp of the record.
            model (str): Model identifier used.
            message_length (int): Length of the message.
            response_time (float): Response time in seconds.
            tokens_used (int): Number of tokens consumed.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO analytics_messages
            (timestamp, model, message_length, response_time, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, model, message_length, response_time, tokens_used))
        conn.commit()

    def get_analytics_history(self):
        """
        Retrieve all analytics history from database.

        Returns:
            list: List of tuples containing analytics records, sorted by
                timestamp in ascending order.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, model, message_length, response_time, tokens_used
            FROM analytics_messages
            ORDER BY timestamp ASC
        ''')
        return cursor.fetchall()

    def __del__(self):
        """
        Cleanup database connections on object destruction.

        Closes thread-local database connection to prevent resource leaks.
        """
        if hasattr(self.local, 'connection'):
            self.local.connection.close()

    def clear_history(self):
        """
        Clear all chat history from database.

        Deletes all records from the messages table, effectively
        clearing the entire chat history.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages')
        conn.commit()

    def get_formatted_history(self):
        """
        Retrieve formatted chat history as list of dictionaries.

        Returns:
            list[dict]: List of dictionaries containing message data with keys:
                - id (int): Message identifier
                - model (str): Model identifier used
                - user_message (str): User's message text
                - ai_response (str): AI model's response text
                - timestamp (datetime): Message timestamp
                - tokens_used (int): Number of tokens consumed

        Messages are sorted by timestamp in ascending order (oldest first).
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                id,
                model,
                user_message,
                ai_response,
                timestamp,
                tokens_used
            FROM messages
            ORDER BY timestamp ASC
        ''')

        history = []
        for row in cursor.fetchall():
            history.append({
                "id": row[0],
                "model": row[1],
                "user_message": row[2],
                "ai_response": row[3],
                "timestamp": row[4],
                "tokens_used": row[5]
            })
        return history
