from configurations.constants import Log_Folder, Log_Level, config
import logging
import json
import os


class LoggerUtility:
    def __init__(self, module, configuration=config):
        if os.path.exists(configuration):
            with open(configuration, 'r') as c:
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