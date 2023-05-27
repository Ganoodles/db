import logging
from colorama import Fore, Style

logger = logging.getLogger("bot_logger")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter for console output
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname.lower()
        color = None
        
        match level:
            case "info":
                color = Fore.LIGHTGREEN_EX
            case "warning":
                color = Fore.YELLOW
            case "error":
                color = Fore.LIGHTRED_EX
            case "critical":
                color = Fore.RED
            case "debug":
                color = Fore.LIGHTBLUE_EX

        message = f"{record.levelname}: {record.getMessage()}"
        formatted_message = f"{color}{message}{Style.RESET_ALL}"
        return formatted_message

console_formatter = ColoredFormatter("%(message)s")
console_handler.setFormatter(console_formatter)

# Create a formatter for file output
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class Logger:
    def __init__(self):
        pass

    def log(self, level, message):
        logger.log(level, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def warning(self, message):
        self.log(logging.WARNING, message)
        
    def critical(self, message):
        self.log(logging.CRITICAL, message)

    def debug(self, message):
        self.log(logging.DEBUG, message)