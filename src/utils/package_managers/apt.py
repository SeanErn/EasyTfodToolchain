# File: utils/package_managers/apt.py

import logging
from typing import List

logger = logging.getLogger(__name__)

def setup_system(sudo_password: str) -> List[str]:
    error_message = "APT package manager installation has not been implemented yet."
    logger.error(error_message)
    return [error_message]

def add_repository(repo: str, sudo_password: str) -> str:
    error_message = "APT package manager installation has not been implemented yet."
    logger.error(error_message)
    return error_message

def install_package(package_name: str, sudo_password: str) -> str:
    error_message = "APT package manager installation has not been implemented yet."
    logger.error(error_message)
    return error_message

def update_package_lists(sudo_password: str) -> str:
    error_message = "APT package manager installation has not been implemented yet."
    logger.error(error_message)
    return error_message