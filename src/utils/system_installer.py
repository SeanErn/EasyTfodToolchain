# File: utils/system_installer.py

import subprocess
import shutil
import logging
from typing import Callable

logger = logging.getLogger()

class SystemPackageInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.package_manager = self._detect_package_manager()

    def _detect_package_manager(self):
        package_managers = {
            "apt-get": "apt-get",
            "dnf": "dnf",
            "yum": "yum",
            "pacman": "pacman",
            "zypper": "zypper",
            "apk": "apk"
        }
        
        for pm, command in package_managers.items():
            if shutil.which(command):
                return pm
        
        return None

    def install_package(self, package_name):
        if not self.package_manager:
            return f"Unable to detect package manager. Please install {package_name} manually."

        commands = {
            "apt-get": f"apt-get install -y {package_name}",
            "dnf": f"dnf install -y {package_name}",
            "yum": f"yum install -y {package_name}",
            "pacman": f"pacman -S --noconfirm {package_name}",
            "zypper": f"zypper install -y {package_name}",
            "apk": f"apk add {package_name}"
        }

        command = commands.get(self.package_manager)
        if not command:
            return f"Unsupported package manager. Please install {package_name} manually."

        sudo_command = f"sudo -S {command}"

        try:
            logger.debug(f"Attempting to install {package_name}")
            process = subprocess.Popen(
                sudo_command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send the sudo password
            stdout, stderr = process.communicate(input=f"{self.sudo_password}\n")
            
            for line in stdout.splitlines():
                self.log_write(line.strip())
            
            for line in stderr.splitlines():
                logger.error(line.strip())
                self.log_write(f"[red]{line.strip()}[/red]")
            
            if process.returncode == 0:
                logger.debug(f"Successfully installed {package_name}")
                return f"Successfully installed {package_name}"
            else:
                logger.error(f"Failed to install {package_name}")
                return f"Failed to install {package_name}"
        except Exception as e:
            logger.exception(f"Error installing {package_name}")
            return f"Error installing {package_name}: {str(e)}"