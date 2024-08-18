# File: main.py

import logging
import sys
import argparse
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

def parse_arguments():
    parser = argparse.ArgumentParser(description="EasyTfodToolchain Installer")
    parser.add_argument("--skip-system", action="store_true", help="Skip system package installation")
    parser.add_argument("--skip-tfod", action="store_true", help="Skip TensorFlow Object Detection API installation")
    return parser.parse_args()

def main():
    args = parse_arguments()
    setup_logging()
    
    if args.skip_system:
        logging.warning("SYSTEM PACKAGE INSTALLATION WILL BE SKIPPED")
    if args.skip_tfod:
        logging.warning("TENSORFLOW OBJECT DETECTION API INSTALLATION WILL BE SKIPPED")
    
    logging.info("Starting the application")
    logging.info(f"Skip system installation: {args.skip_system}")
    logging.info(f"Skip TFOD installation: {args.skip_tfod}")
    
    try:
        app = EasyTfodToolchainInstaller(skip_system=args.skip_system, skip_tfod=args.skip_tfod)
        logging.info("Running the application")
        app.run()
    except Exception as e:
        logging.exception(f"An error occurred while running the application: {str(e)}")
    finally:
        logging.info("Application finished")

if __name__ == "__main__":
    main()