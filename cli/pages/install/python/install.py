import subprocess
from subprocess import Popen

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import (
    Button,
    Footer,
    Header,
    Static,
    MarkdownViewer,
    ProgressBar,
    RichLog,
)
from textual.reactive import Reactive
from textual.screen import Screen, ModalScreen
from textual.containers import Vertical
from pathlib import Path
from cli.shared.workflowTabs import WorkflowTabs
import sys
import threading
import os


class LogInstall(ModalScreen):
    BINDINGS = [
        ("l", "toggle_log", "Toggles the log viewer"),
        ("r", "refresh_log", "Refreshes the log viewer"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(), RichLog(highlight=True, id="installLog"), id="installLogContainer"
        )

    def on_mount(self) -> None:
        self.title = "Log Viewer"
        self.sub_title = "Press R to refresh log"
        self.action_refresh_log()

    def action_refresh_log(self) -> None:
        log_files = Path("logs").glob("_install_*.log")
        log_files = list(log_files)

        if log_files:
            most_recent_log = max(log_files, key=os.path.getctime)
            self.query_one(RichLog).clear()
            self.query_one(RichLog).write(most_recent_log.read_text())
        else:
            self.query_one(RichLog).write("No logs exist!")

    def action_toggle_log(self) -> None:
        self.app.pop_screen()


class Install(Screen):
    logScreenActive: bool
    BINDINGS = [("l", "toggle_log", "Toggles the log viewer")]

    def compose(self) -> ComposeResult:
        yield Vertical(
            WorkflowTabs(), InstallContent(), InstallButtons(), id="installContainer"
        )

    def action_toggle_log(self) -> None:
        self.logScreenActive = True
        self.app.push_screen(LogInstall())


class InstallContent(Static):
    """content of install screen"""

    #   logPipe = Reactive("Press start to start the installation.")
    def compose(self) -> ComposeResult:
        yield MarkdownViewer(
            Path("cli/pages/install/md/install.md").read_text(),
            show_table_of_contents=False,
        )


class InstallButtons(Static):
    """Install widget"""

    process: Popen[bytes]
    BINDINGS = [
        ("space", "start_install", "Start the install"),
        ("q", "cancel_install", "Stops the install"),
    ]
    started = False

    def action_start_install(self) -> None:
        # Check if subprocess is already running
        if self.started:
            print("Install already running...")
            return
        else:
            self.started = True
            print("Starting new thread")
            threading.Thread(target=self.run_bash_script).start()
            self.query_one(ProgressBar).progress = 0
            self.query("#startBtn").remove()

    def action_cancel_install(self) -> None:
        try:
            self.process.terminate()
        except AttributeError:
            print("Subprocess not running...")
        sys.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "startBtn":
            self.action_start_install()
        if event.button.id == "cancelBtn":
            self.action_cancel_install()

    def run_bash_script(self):
        # Run the bash script
        self.process = subprocess.Popen(
            ["./install/install.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Read the output in real-time
        while True:
            # Check if the bash script has finished executing
            if self.process.poll() is not None:
                break

            # Try to read a line of output from the bash script
            output = self.process.stdout.readline()
            if output:
                output = output.strip().decode()
                #  self.logPipe = output
                if output.startswith("prog"):
                    # Remove the 'prog' prefix and print the progress
                    progress = output[4:]  # Slice the string from the 4th character
                    self.query_one(ProgressBar).progress = float(progress)

                    if progress == "Done":
                        self.query("#cancelBtn").remove()

    def compose(self) -> ComposeResult:
        """Child widgets of install"""
        yield ProgressBar(total=100, id="installProgress", show_eta=False)
        yield Button("Start", id="startBtn", variant="success")
        yield Button("Exit", id="cancelBtn", variant="error")
