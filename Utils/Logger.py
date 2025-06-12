from configurations.constants import Log_Folder, Log_Level, config
import logging
import json
import os


class LoggerUtility:
    def __init__(self, module, configuration=None):
        """Logger utility to write timestamped log messages to a specified log file.

    Args:
        module (str): Module name whose logging configuration should be used.
        configuration (dict, optional): Direct configuration dictionary.
                                        If not provided, configuration is loaded from 'config.json' using the module key.

    Attributes:
        logfile_path (str): Full path to the log file.
        logger (Logger): Python logging object configured with file handler and formatter.

    Methods:
        log(message: str, level: str = "info"):
            Logs a message with a timestamp using the specified log level.

    Example:
        >>> logger_util = LoggerUtility("booking_module")
        >>> logger_util.log("Booking module initialized", level="info")

        Or, using a direct configuration dictionary:
        >>> config = {"loging_dir": "logs", "logfile_path": "booking.log"}
        >>> logger_util = LoggerUtility("booking_module", config)
        >>> logger_util.log("Booking created", level="debug")

    Notes:
        - If configuration is not passed, it attempts to read from 'config.json' and use the module-specific config.
        - Automatically creates the log directory if it doesn't exist.
        - Supported log levels: 'info', 'warning', 'error', 'debug'.
"""
        if not configuration:
            with open(config, 'r') as c:
                configuration = json.load(c)
                configuration = configuration.get(module)

        self.logfile_path = os.path.join(configuration.get("loging_dir", Log_Folder),
                                         configuration.get("logfile_path", "app.log"))
        self.logger = self._setup_logger()

    def _setup_logger(self):
        # Ensure the log directory exists
        log_dir = os.path.dirname(self.logfile_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            file_handler = logging.FileHandler(self.logfile_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def log(self, message, level=Log_Level):
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)
        else:
            self.logger.info(message)