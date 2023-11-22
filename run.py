from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Markdown
from pathlib import Path
import sys
from cli.python.install import Install, InstallButtons
class RunToolkit(App):
    """Main UI of Toolkit"""

    CSS_PATH = ["cli/css/install.tcss"]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit the app")]

    def on_mount(self) -> None:
        self.push_screen(Install())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit(self) -> None:
        """An action to quit the app. DOES NOT STOP THE INSTALLATION IF STARTED"""
        sys.exit(0)

if __name__ == "__main__":
    app = RunToolkit()
    app.run()