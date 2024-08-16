# File: utils/threaded_installer.py

import threading
import logging
from typing import Callable, List
from utils.system_installer import SystemPackageInstaller

class ThreadedInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.installer = SystemPackageInstaller(log_write, sudo_password)
        self.installation_thread = None
        self.is_installing = False
        logging.info("ThreadedInstaller initialized")

    def start_installation(self, packages: List[str], on_complete: Callable[[], None]):
        if self.is_installing:
            logging.warning("Installation already in progress")
            self.log_write("[yellow]Installation is already in progress.[/yellow]")
            return

        logging.info(f"Starting threaded installation of {len(packages)} packages")
        self.is_installing = True
        self.installation_thread = threading.Thread(
            target=self._run_installation,
            args=(packages, on_complete)
        )
        self.installation_thread.start()

    def _run_installation(self, packages: List[str], on_complete: Callable[[], None]):
        try:
            for package in packages:
                if not self.is_installing:
                    logging.info("Installation cancelled")
                    self.log_write("[red]Installation cancelled.[/red]")
                    break
                self.log_write(f"[yellow]Installing {package}...[/yellow]")
                result = self.installer.install_package(package)
                self.log_write(result)

            if self.is_installing:
                self.log_write("[green]Installation complete![/green]")
                logging.info("Installation process completed")
        except Exception as e:
            logging.exception(f"Error during package installation: {str(e)}")
            self.log_write(f"[red]An error occurred during package installation: {str(e)}[/red]")
        finally:
            self.is_installing = False
            on_complete()

    def cancel_installation(self):
        if self.is_installing:
            logging.info("Cancelling installation")
            self.is_installing = False
            if self.installation_thread:
                self.installation_thread.join()
            self.log_write("[yellow]Installation cancelled.[/yellow]")