# File: app.py

import logging
from textual.app import App
from textual.widgets import Footer
from screens.installer_screen import InstallerScreen

class EasyTfodToolchainInstaller(App):
    CSS_PATH = ["styles/main.css", "styles/installer_screen.css"]
    SCREENS = {"installer": InstallerScreen()}
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info("EasyTfodToolchainInstaller initialized")

    def on_mount(self) -> None:
        logging.info("EasyTfodToolchainInstaller mounted")
        try:
            self.push_screen("installer")
        except Exception as e:
            logging.exception(f"Error pushing installer screen: {str(e)}")

    def on_load(self) -> None:
        logging.info("EasyTfodToolchainInstaller loaded")

    def on_exit(self) -> None:
        logging.info("EasyTfodToolchainInstaller exiting")

    def compose(self):
        logging.debug("Composing main app layout")
        yield Footer()