# File: main.py

import logging
import sys
from textual.app import App
from app import EasyTfodToolchainInstaller

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # File Handler
    file_handler = logging.FileHandler("app.log", mode="w")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

def main():
    setup_logging()
    logging.info("Starting the application")
    
    try:
        app = EasyTfodToolchainInstaller()
        logging.info("Running the application")
        app.run()
    except Exception as e:
        logging.exception(f"An error occurred while running the application: {str(e)}")
    finally:
        logging.info("Application finished")

if __name__ == "__main__":
    main()