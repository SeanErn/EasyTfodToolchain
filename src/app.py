# File: app.py

import logging
from textual.app import App
from textual.widgets import Footer
from screens.installer_screen import InstallerScreen

logger = logging.getLogger()

class EasyTfodToolchainInstaller(App):
    CSS_PATH = ["styles/main.css", "styles/installer_screen.css"]
    SCREENS = {"installer": InstallerScreen()}
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("EasyTfodToolchainInstaller initialized")

    def on_mount(self) -> None:
        logger.info("EasyTfodToolchainInstaller mounted")
        try:
            self.push_screen("installer")
        except Exception as e:
            logger.exception(f"Error pushing installer screen: {str(e)}")

    def on_load(self) -> None:
        logger.info("EasyTfodToolchainInstaller loaded")

    def on_exit(self) -> None:
        logger.info("EasyTfodToolchainInstaller exiting")

    def compose(self):
        logger.debug("Composing main app layout")
        yield Footer()