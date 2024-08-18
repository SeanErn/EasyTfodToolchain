# File: utils/threaded_installer.py

import threading
import queue
import asyncio
import logging
from typing import Callable
from utils.system_installer import SystemPackageInstaller
from utils.tensorflow_installer import TensorFlowInstaller

logger = logging.getLogger(__name__)

class ThreadedInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str, skip_system: bool = False, skip_tfod: bool = False):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.skip_system = skip_system
        self.skip_tfod = skip_tfod
        self.system_installer = SystemPackageInstaller(self._queue_log_write, sudo_password)
        self.tensorflow_installer = TensorFlowInstaller(self._queue_log_write)
        self.installation_thread = None
        self.is_installing = False
        self.message_queue = queue.Queue()
        logger.info("ThreadedInstaller initialized")
        logger.info(f"Skip system installation: {self.skip_system}")
        logger.info(f"Skip TFOD installation: {self.skip_tfod}")

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

            if self.skip_system:
                logger.warning("Skipping system setup")
                self._queue_log_write("[yellow]WARNING: Skipping system package installation.[/yellow]")
            else:
                logger.info("Running system setup")
                self.system_installer.setup_system()

            if self.skip_tfod:
                logger.warning("Skipping TensorFlow Object Detection API installation")
                self._queue_log_write("[yellow]WARNING: Skipping TensorFlow Object Detection API installation.[/yellow]")
            else:
                logger.info("Running TensorFlow Object Detection API installation")
                self.tensorflow_installer.run_installation()

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

        self.log_write("[green]Installation complete![/green]")
        logger.info("Installation process completed")
        on_complete()

    def cancel_installation(self):
        if self.is_installing:
            logger.info("Cancelling installation")
            self.is_installing = False
            self._queue_log_write("[yellow]Installation cancelled.[/yellow]")
            if self.installation_thread:
                self.installation_thread.join() 