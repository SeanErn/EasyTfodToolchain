from textual.app import ComposeResult
from textual.widgets import Tabs, Tab, Static


class WorkflowTabs(Static):
    """Tabs for selection current part of workflow"""

    def compose(self) -> ComposeResult:
        yield Tabs(
            Tab("Install", id="installTab"),
            Tab("Project Manager", id="managerTab"),
            Tab("Annotate", id="annotateTab"),
            Tab("Prepare Dataset", id="prepareTab"),
            Tab("Train Model", id="trainTab"),
            Tab("Export Model", id="exportTab"),
            Tab("Test Model", id="testTab"),
            Tab("Advanced", id="advancedTab"),
            Tab("Exit", id="exitTab"),
        )
