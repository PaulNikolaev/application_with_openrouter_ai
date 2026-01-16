"""
Performance monitoring utility module.

This module provides system performance monitoring capabilities for the application.
It tracks CPU usage, memory consumption, thread count, and application uptime,
with health checking and metrics history management.
"""
import time
from datetime import datetime

import psutil


class PerformanceMonitor:
    """
    Application performance monitoring system.

    Tracks and analyzes system resource usage including CPU, memory, thread count,
    and application uptime. Provides health checking based on configurable thresholds
    and maintains metrics history for analysis.

    Attributes:
        start_time (float): Monitoring start timestamp.
        metrics_history (list): History of collected metrics (max 1000 entries).
        process (psutil.Process): Current process object for metrics collection.
        thresholds (dict): Threshold values for health checking.
    """

    def __init__(self):
        """
        Initialize performance monitoring system.

        Sets up monitoring start time, metrics history storage, process tracking,
        and configurable threshold values for health checking.
        """
        self.start_time = time.time()
        self.metrics_history = []
        self.process = psutil.Process()

        # Threshold values for performance issue detection
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 75.0,
            'thread_count': 50
        }

    def get_metrics(self) -> dict:
        """
        Get current performance metrics.

        Collects and returns current system metrics including CPU usage,
        memory consumption, thread count, and application uptime.
        Automatically saves metrics to history (limited to 1000 entries).

        Returns:
            dict: Dictionary containing current metrics:
                - timestamp (datetime): Measurement timestamp
                - cpu_percent (float): CPU usage percentage
                - memory_percent (float): Memory usage percentage
                - thread_count (int): Number of active threads
                - uptime (float): Application uptime in seconds

            If an error occurs, returns dict with 'error' key.

        Note:
            Metrics history is automatically limited to the last 1000 entries.
        """
        try:
            metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': self.process.cpu_percent(),
                'memory_percent': self.process.memory_percent(),
                'thread_count': len(self.process.threads()),
                'uptime': time.time() - self.start_time
            }

            # Save to history and limit to last 1000 entries
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)

            return metrics

        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now()
            }

    def check_health(self) -> dict:
        """
        Check system health based on threshold values.

        Analyzes current metrics and compares them against configured thresholds
        to identify potential performance issues.

        Returns:
            dict: Dictionary containing health status information:
                - status (str): 'healthy', 'warning', or 'error'
                - warnings (list): List of warning messages (if any)
                - timestamp (datetime): Health check timestamp
                - error (str): Error message (if status is 'error')
        """
        metrics = self.get_metrics()

        if 'error' in metrics:
            return {'status': 'error', 'error': metrics['error']}

        health_status = {
            'status': 'healthy',
            'warnings': [],
            'timestamp': metrics['timestamp']
        }

        # Check CPU usage threshold
        if metrics['cpu_percent'] > self.thresholds['cpu_percent']:
            health_status['warnings'].append(
                f"High CPU usage: {metrics['cpu_percent']}%"
            )
            health_status['status'] = 'warning'

        # Check memory usage threshold
        if metrics['memory_percent'] > self.thresholds['memory_percent']:
            health_status['warnings'].append(
                f"High memory usage: {metrics['memory_percent']}%"
            )
            health_status['status'] = 'warning'

        # Check thread count threshold
        if metrics['thread_count'] > self.thresholds['thread_count']:
            health_status['warnings'].append(
                f"High thread count: {metrics['thread_count']}"
            )
            health_status['status'] = 'warning'

        return health_status

    def get_average_metrics(self) -> dict:
        """
        Calculate average metrics over entire observation history.

        Computes average values for CPU usage, memory usage, and thread count
        based on all collected metrics in history.

        Returns:
            dict: Dictionary containing average metrics:
                - avg_cpu (float): Average CPU usage percentage
                - avg_memory (float): Average memory usage percentage
                - avg_threads (float): Average thread count
                - samples_count (int): Number of samples analyzed

            Returns dict with 'error' key if no metrics are available.
        """
        if not self.metrics_history:
            return {"error": "No metrics available"}

        avg_metrics = {
            'avg_cpu': sum(m['cpu_percent'] for m in self.metrics_history) / len(self.metrics_history),
            'avg_memory': sum(m['memory_percent'] for m in self.metrics_history) / len(self.metrics_history),
            'avg_threads': sum(m['thread_count'] for m in self.metrics_history) / len(self.metrics_history),
            'samples_count': len(self.metrics_history)
        }

        return avg_metrics

    def log_metrics(self, logger) -> None:
        """
        Log current metrics and system health status.

        Writes performance metrics and health warnings to the provided logger.

        Args:
            logger: Logger instance for writing log messages.
        """
        metrics = self.get_metrics()
        health = self.check_health()

        # Log current performance metrics
        if 'error' not in metrics:
            logger.info(
                f"Performance metrics - "
                f"CPU: {metrics['cpu_percent']:.1f}%, "
                f"Memory: {metrics['memory_percent']:.1f}%, "
                f"Threads: {metrics['thread_count']}, "
                f"Uptime: {metrics['uptime']:.0f}s"
            )

        # Log warnings if performance issues detected
        if health['status'] == 'warning':
            for warning in health['warnings']:
                logger.warning(f"Performance warning: {warning}")
