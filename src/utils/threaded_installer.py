# File: utils/threaded_installer.py

import threading
import queue
import asyncio
import logging
from typing import Callable
from utils.system_installer import SystemPackageInstaller

logger = logging.getLogger(__name__)

class ThreadedInstaller:
    def __init__(self, log_write: Callable[[str], None], sudo_password: str):
        self.log_write = log_write
        self.sudo_password = sudo_password
        self.installer = SystemPackageInstaller(self._queue_log_write, sudo_password)
        self.installation_thread = None
        self.is_installing = False
        self.message_queue = queue.Queue()
        logger.info("ThreadedInstaller initialized")

    def _queue_log_write(self, message: str):
        self.message_queue.put(message)

    def start_installation(self, on_complete: Callable[[], None]):
        if self.is_installing:
            logger.warning("Installation already in progress")
            self.log_write("[yellow]Installation is already in progress.[/yellow]")
            return

        logger.info("Starting threaded system setup")
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

            logger.info("Running system setup")
            self.installer.setup_system()
        except Exception as e:
            logger.exception(f"Error during system setup: {str(e)}")
            self._queue_log_write(f"[red]An error occurred during system setup: {str(e)}[/red]")
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

        self.log_write("[green]System setup complete![/green]")
        logger.info("System setup process completed")
        on_complete()

    def cancel_installation(self):
        if self.is_installing:
            logger.info("Cancelling installation")
            self.is_installing = False
            self._queue_log_write("[yellow]Installation cancelled.[/yellow]")
            if self.installation_thread:
                self.installation_thread.join()