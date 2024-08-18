# File: app.py

import logging
from textual.app import App
from textual.widgets import Footer
from screens.installer_screen import InstallerScreen

logger = logging.getLogger()

class EasyTfodToolchainInstaller(App):
    CSS_PATH = [
        "styles/main.css",
        "styles/content.css",
        "styles/log_container.css",
        "styles/footer.css",
        "styles/installer_screen.css",
        "styles/password_dialog.css"
    ]
    SCREENS = {"installer": InstallerScreen()}
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, skip_system=False, skip_tfod=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_system = skip_system
        self.skip_tfod = skip_tfod
        logger.info("EasyTfodToolchainInstaller initialized")
        logger.info(f"Skip system installation: {self.skip_system}")
        logger.info(f"Skip TFOD installation: {self.skip_tfod}")

    def on_mount(self) -> None:
        logger.info("EasyTfodToolchainInstaller mounted")
        try:
            installer_screen = self.SCREENS["installer"]
            installer_screen.skip_system = self.skip_system
            installer_screen.skip_tfod = self.skip_tfod
            self.push_screen(installer_screen)
        except Exception as e:
            logger.exception(f"Error pushing installer screen: {str(e)}")

    def on_load(self) -> None:
        logger.info("EasyTfodToolchainInstaller loaded")

    def on_exit(self) -> None:
        logger.info("EasyTfodToolchainInstaller exiting")

    def compose(self):
        logger.debug("Composing main app layout")
        yield Footer()