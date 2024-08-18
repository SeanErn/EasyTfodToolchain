# File: utils/threaded_installer.py

import threading
import queue
import asyncio
import logging
from typing import Callable
from utils.system_installer import SystemPackageInstaller
from utils.tfod_installer import TFODInstaller

logger = logging.getLogger(__name__)

class ThreadedInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str, skip_system_install=False, skip_tfod_install=False):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.skip_system_install = skip_system_install
        self.skip_tfod_install = skip_tfod_install
        self.system_installer = SystemPackageInstaller(self._queue_log_write, sudo_password)
        self.tfod_installer = TFODInstaller(self._queue_log_write)
        self.installation_thread = None
        self.is_installing = False
        self.message_queue = queue.Queue()
        logger.info("ThreadedInstaller initialized")
        logger.info(f"Skip system install: {self.skip_system_install}")
        logger.info(f"Skip TFOD install: {self.skip_tfod_install}")

    def _queue_log_write(self, message: str):
        self.message_queue.put(message)

    def start_installation(self, on_complete: Callable[[], None]):
        if self.is_installing:
            logger.warning("Installation already in progress")
            self.log_write("[yellow]Installation is already in progress.[/yellow]")
            return

        logger.info("Starting threaded installation")
        self.is_installing = True
        self.installation_thread = threading.Thread(target=self._run_installation)
        self.installation_thread.start()

        # Start the message processing coroutine
        asyncio.create_task(self._process_messages(on_complete))

    def _run_installation(self):
        try:
            if not self.is_installing:
                logger.info("Installation cancelled before it began")
                self._queue_log_write("[red]Installation cancelled.[/red]")
                return

            if not self.skip_system_install:
                logger.info("Running system setup")
                self._queue_log_write("[blue]Starting system package installation...[/blue]")
                self.system_installer.setup_system()
                self._queue_log_write("[green]System package installation completed.[/green]")
            else:
                logger.info("Skipping system package installation")
                self._queue_log_write("[yellow]Skipping system package installation.[/yellow]")

            if not self.skip_tfod_install:
                logger.info("Running TFOD installation")
                self._queue_log_write("[blue]Starting TensorFlow Object Detection API installation...[/blue]")
                self.tfod_installer.run_installation()
                self._queue_log_write("[green]TensorFlow Object Detection API installation completed.[/green]")
            else:
                logger.info("Skipping TFOD installation")
                self._queue_log_write("[yellow]Skipping TensorFlow Object Detection API installation.[/yellow]")

        except Exception as e:
            logger.exception(f"Error during installation: {str(e)}")
            self._queue_log_write(f"[red]An error occurred during installation: {str(e)}[/red]")
        finally:
            self.is_installing = False
            self._queue_log_write("INSTALLATION_COMPLETE")

    async def _process_messages(self, on_complete: Callable[[], None]):
        while self.is_installing or not self.message_queue.empty():
            try:
                message = self.message_queue.get_nowait()
                if message == "INSTALLATION_COMPLETE":
                    break
                self.log_write(message)
            except queue.Empty:
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

        self.log_write("[green]Installation process complete![/green]")
        logger.info("Installation process completed")
        on_complete()

    def cancel_installation(self):
        if self.is_installing:
            logger.info("Cancelling installation")
            self.is_installing = False
            self._queue_log_write("[yellow]Installation cancelled.[/yellow]")
            if self.installation_thread:
                self.installation_thread.join()

logger.info("ThreadedInstaller module loaded")