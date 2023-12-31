import subprocess
import sys

from cli.pages.install.python.dependencyChecker import meets_min_requirements

# User must be sudo to run program
subprocess.run(["/usr/bin/sudo", "-v"])

# Check for minimum requirements
if not meets_min_requirements():
    print(
        "Hang tight! We are installing dependencies for you. (This may take a while depending on your internet speed)"
    )
    process = subprocess.Popen(
        ["./installDependencies.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    process.wait()
    sys.exit(
        "Dependencies have been installed. Please restart your terminal and run this program again."
    )
# Run rest as normal
from textual.app import App
from cli.pages.install.python.install import Install


class RunToolkit(App):
    """Main UI of Toolkit"""

    CSS_PATH = ["cli/pages/install/css/install.tcss"]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit the app")]

    def on_mount(self) -> None:
        self.push_screen(Install())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    @staticmethod
    def action_quit() -> None:
        """An action to quit the app. DOES NOT STOP THE INSTALLATION IF STARTED"""
        sys.exit(0)


if __name__ == "__main__":
    app = RunToolkit()
    app.run()
