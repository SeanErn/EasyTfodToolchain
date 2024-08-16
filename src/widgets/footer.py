# File: widgets/footer.py

import logging
from textual.widgets import Static, Button
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message

logger = logging.getLogger()

class InstallerFooter(Static):
    DEFAULT_CSS = """
    InstallerFooter {
        height: 3;
        background: $panel;
        padding: 0 1;
    }
    InstallerFooter Horizontal {
        width: 100%;
        height: 100%;
        align: left middle;
    }
    InstallerFooter Button {
        margin: 0 1;
        min-width: 10;
    }
    """

    class InstallRequested(Message):
        """A message sent when the Install button is pressed."""

    class ExitRequested(Message):
        """A message sent when the Exit button is pressed."""

    def compose(self):
        yield Horizontal(
            Button("Install", variant="success", id="install"),
            Button("Exit", variant="error", id="exit"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "install":
            logger.info("Install button pressed")
            self.post_message(self.InstallRequested())
        elif event.button.id == "exit":
            logger.info("Exit button pressed")
            self.post_message(self.ExitRequested())

    def on_mount(self):
        logger.info("InstallerFooter mounted")