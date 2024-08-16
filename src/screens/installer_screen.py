# File: screens/installer_screen.py

import logging
import asyncio
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Static
from textual.widgets import RichLog
from widgets.footer import InstallerFooter
from widgets.password_dialog import PasswordDialog
from utils.threaded_installer import ThreadedInstaller

logger = logging.getLogger(__name__)

class InstallerScreen(Screen):
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log = None
        self._sudo_password = None
        self._threaded_installer = None
        self._password_future = None
        logger.info("InstallerScreen initialized")

    def compose(self) -> ComposeResult:
        logger.debug("Composing InstallerScreen")
        try:
            yield Header()
            yield Vertical(
                Container(
                    Static("Welcome to EasyTfodToolchain Installer", id="title"),
                    Static("This tool will help you set up the TensorFlow Object Detection environment.", id="description"),
                    id="content",
                ),
                RichLog(id="log", markup=True),
                id="main_container"
            )
            yield InstallerFooter()
        except Exception as e:
            logger.exception(f"Error composing InstallerScreen: {str(e)}")
            raise

    def on_mount(self):
        try:
            self._log = self.query_one("#log")
            logger.info("InstallerScreen mounted")
            self._log_write("[green]Welcome to the EasyTfodToolchain Installer![/green]")
            self._log_write("This log will show the progress of the installation.")
            self.adjust_log_height()
        except Exception as e:
            logger.exception(f"Error in InstallerScreen on_mount: {str(e)}")

    def on_installer_footer_install_requested(self, message: InstallerFooter.InstallRequested) -> None:
        try:
            if not self._threaded_installer or not self._threaded_installer.is_installing:
                logger.info("Install requested from footer")
                self._log_write("[blue]Install requested. Starting installation process...[/blue]")
                asyncio.create_task(self.run_installation())
            else:
                logger.info("Installation already in progress")
                self._log_write("[yellow]Installation is already in progress.[/yellow]")
        except Exception as e:
            logger.exception(f"Error handling install request from footer: {str(e)}")
            self._log_write(f"[red]An error occurred: {str(e)}[/red]")

    def on_installer_footer_exit_requested(self, message: InstallerFooter.ExitRequested) -> None:
        try:
            logger.info("Exit requested from footer")
            if self._threaded_installer and self._threaded_installer.is_installing:
                self._log_write("[yellow]Cancelling installation...[/yellow]")
                self._threaded_installer.cancel_installation()
            self.app.exit()
        except Exception as e:
            logger.exception(f"Error handling exit request from footer: {str(e)}")
            self._log_write(f"[red]An error occurred while exiting: {str(e)}[/red]")

    async def run_installation(self) -> None:
        try:
            logger.info("Prompting for sudo password")
            self._log_write("Please enter your sudo password to proceed with the installation.")
            password = await self.get_password()
            if password:
                logger.info("Password received, starting installation")
                self._log_write("[green]Password received. Starting system setup...[/green]")
                self._sudo_password = password
                await self.setup_system()
            else:
                logger.warning("No password provided")
                self._log_write("[red]Installation cancelled: No password provided.[/red]")
        except Exception as e:
            logger.exception(f"Error running installation: {str(e)}")
            self._log_write(f"[red]An error occurred while starting the installation: {str(e)}[/red]")

    async def get_password(self):
        self._password_future = asyncio.Future()
        self.app.push_screen(PasswordDialog(), callback=self.on_password_entered)
        return await self._password_future

    def on_password_entered(self, password: str):
        if not self._password_future.done():
            self._password_future.set_result(password)

    async def setup_system(self) -> None:
        try:
            logger.info("Starting system setup")
            self._log_write("[green]Starting system setup...[/green]")
            
            self._threaded_installer = ThreadedInstaller(self._log_write, self._sudo_password)
            self._threaded_installer.start_installation(self.on_installation_complete)
        except Exception as e:
            logger.exception(f"Error during system setup: {str(e)}")
            self._log_write(f"[red]An error occurred during system setup: {str(e)}[/red]")
        finally:
            self._sudo_password = None  # Clear the password after use

    def on_installation_complete(self):
        logger.info("Installation process completed")
        self._log_write("[green]Installation process completed![/green]")
        self._threaded_installer = None

    def on_resize(self) -> None:
        logger.debug("InstallerScreen resized")
        self.adjust_log_height()

    def adjust_log_height(self) -> None:
        try:
            main_container = self.query_one("#main_container")
            content = self.query_one("#content")
            log = self.query_one("#log")
            
            content_height = content.region.height
            available_height = main_container.region.height - content_height
            log.styles.height = available_height
            logger.debug(f"Adjusted log height to {available_height}")
        except Exception as e:
            logger.exception(f"Error adjusting log height: {str(e)}")

    def _log_write(self, message: str):
        """Helper method to write to log with proper formatting."""
        self._log.write(message)