import subprocess
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
    Tabs,
    Tab,
    TextArea,
)
from textual.reactive import Reactive
from textual.screen import Screen, ModalScreen
from textual.containers import Grid
from pathlib import Path
from cli.shared.workflowTabs import WorkflowTabs
import sys
import threading
import os


class LogDash(ModalScreen):
    BINDINGS = [
        ("l", "toggle_log", "Toggles the log viewer"),
        ("r", "refresh_log", "Refreshes the log viewer"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(), RichLog(highlight=True, id="dashLog"), id="dashLogContainer"
        )

    def on_mount(self) -> None:
        self.title = "Log Viewer"
        self.sub_title = "Press R to refresh log"
        self.action_refresh_log()

    def action_refresh_log(self) -> None:
        log_files = Path("logs").glob("_main_*.log")
        log_files = list(log_files)

        if log_files:
            most_recent_log = max(log_files, key=os.path.getctime)
            self.query_one(RichLog).clear()
            self.query_one(RichLog).write(most_recent_log.read_text())
        else:
            self.query_one(RichLog).write(
                "No logs exist! (Has Python logging been implemented yet?)"
            )

    def action_toggle_log(self) -> None:
        self.app.pop_screen()


class Dash(Screen):
    BINDINGS = [("l", "toggle_log", "Toggles the log viewer")]

    def compose(self) -> ComposeResult:
        yield Grid(WorkflowTabs(), TextArea("This is dash"), id="dashContainer")

    def action_toggle_log(self) -> None:
        self.logScreenActive = True
        self.app.push_screen(LogInstall())
