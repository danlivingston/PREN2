import os
import sys
import time

from dotenv import load_dotenv
from loguru import logger

from utils import foo

# Load .env file
load_dotenv()


# Automatically catch and log as critical if main loop encounters an unhandled exception
@logger.catch(level="CRITICAL")
def main():
    logger.success("main() executing")
    foo.bar()
    time.sleep(2)
    raise NotImplementedError("main() Not Implemented Yet")


if __name__ == "__main__":
    # Set log file output
    logger.add("logs/debug_{time}.log", enqueue=True, level="TRACE")
    # Replace default logger with stdout (console) based on env level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Defaults to INFO if not set
    logger.remove(0)
    logger.add(sys.stdout, level=LOG_LEVEL)

    # Run the main loop
    logger.info("Starting...")
    main()
    logger.info("Stopping...")
