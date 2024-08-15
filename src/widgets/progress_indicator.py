# File: widgets/progress_indicator.py

import logging
from textual.widget import Widget
from textual.reactive import reactive

class ProgressIndicator(Widget):
    """A simple progress indicator widget."""

    progress = reactive(0.0)
    
    DEFAULT_CSS = """
    ProgressIndicator {
        width: 100%;
        height: 1;
    }
    
    ProgressIndicator > .bar {
        width: 0%;
        height: 100%;
        background: $success;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info("ProgressIndicator initialized")

    def on_mount(self):
        logging.debug("ProgressIndicator mounted")

    def render(self):
        return f'<div class="bar" style="width: {self.progress:.0%}"></div>'

    def update_progress(self, value: float):
        """Update the progress bar."""
        self.progress = max(0.0, min(1.0, value))
        logging.debug(f"Progress updated to {self.progress:.2%}")