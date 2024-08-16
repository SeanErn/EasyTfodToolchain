# File: utils/system_installer.py

import shutil
import logging
from typing import Callable
from utils.package_managers import apt, yum, dnf, pkg

logger = logging.getLogger(__name__)

class SystemPackageInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.package_manager = self._detect_package_manager()
        logger.info(f"Detected package manager: {self.package_manager}")

    def _detect_package_manager(self):
        package_managers = {
            "apt-get": "apt",
            "dnf": "dnf",
            "yum": "yum",
            "pkg": "pkg"
        }
        
        for pm, module_name in package_managers.items():
            if shutil.which(pm):
                return module_name
        
        logger.warning("Unable to detect package manager")
        return None

    def setup_system(self):
        if not self.package_manager:
            logger.error("Unable to detect package manager. Cannot setup system.")
            self.log_write("Unable to detect package manager. Please install packages manually.")
            return

        try:
            installer_module = globals()[self.package_manager]
            installer_module.setup_system(self.sudo_password, self.log_write)
        except Exception as e:
            logger.exception("Error setting up system")
            error_message = f"Error setting up system: {str(e)}"
            self.log_write(error_message)

    def install_package(self, package_name: str):
        if not self.package_manager:
            logger.error(f"Unable to detect package manager. Cannot install {package_name}")
            self.log_write(f"Unable to detect package manager. Please install {package_name} manually.")
            return

        try:
            installer_module = globals()[self.package_manager]
            installer_module.install_package(package_name, self.sudo_password, self.log_write)
        except Exception as e:
            logger.exception(f"Error installing {package_name}")
            error_message = f"Error installing {package_name}: {str(e)}"
            self.log_write(error_message)

    def add_repository(self, repository: str):
        if not self.package_manager:
            logger.error(f"Unable to detect package manager. Cannot add repository {repository}")
            self.log_write(f"Unable to detect package manager. Please add repository {repository} manually.")
            return

        try:
            installer_module = globals()[self.package_manager]
            installer_module.add_repository(repository, self.sudo_password, self.log_write)
        except Exception as e:
            logger.exception(f"Error adding repository {repository}")
            error_message = f"Error adding repository {repository}: {str(e)}"
            self.log_write(error_message)

    def update_package_lists(self):
        if not self.package_manager:
            logger.error("Unable to detect package manager. Cannot update package lists.")
            self.log_write("Unable to detect package manager. Please update package lists manually.")
            return

        try:
            installer_module = globals()[self.package_manager]
            if hasattr(installer_module, 'update_package_lists'):
                installer_module.update_package_lists(self.sudo_password, self.log_write)
            else:
                logger.info("Package list update not required for this package manager.")
                self.log_write("Package list update not required for this package manager.")
        except Exception as e:
            logger.exception("Error updating package lists")
            error_message = f"Error updating package lists: {str(e)}"
            self.log_write(error_message)