# File: main.py

import logging
import sys
from textual.app import App
from app import EasyTfodToolchainInstaller

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log", mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )

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