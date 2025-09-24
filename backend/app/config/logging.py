# logging_config.py
import logging

# Global logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("cooking_agent.log"),  # log file
        logging.StreamHandler()                    # console output
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance for a given module name.

    Args:
        name (str): Usually pass __name__ from the caller module.
    Returns:
        logging.Logger: Logger ready to use.
    """
    return logging.getLogger(name)
