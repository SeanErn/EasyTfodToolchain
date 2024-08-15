# File: widgets/password_dialog.py

import logging
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static

class PasswordDialog(ModalScreen[str]):
    DEFAULT_CSS = """
    PasswordDialog {
        align: center middle;
    }

    #dialog-container {
        width: 60%;
        height: auto;
        border: thick $primary 80%;
        background: $surface;
        padding: 1 2;
    }

    #password-prompt {
        content-align: center middle;
        width: 100%;
        height: 3;
    }

    #password-input {
        width: 100%;
    }

    #submit-button {
        width: 100%;
        margin-top: 1;
    }
    """

    def compose(self):
        logging.debug("Composing PasswordDialog")
        yield Vertical(
            Static("Enter sudo password:", id="password-prompt"),
            Input(password=True, id="password-input"),
            Button("Submit", variant="primary", id="submit-button"),
            id="dialog-container",
        )

    def on_mount(self):
        logging.debug("PasswordDialog mounted")
        self.query_one("#password-input").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-button":
            logging.debug("Submit button pressed in PasswordDialog")
            self._submit_password()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "password-input":
            logging.debug("Password submitted via input in PasswordDialog")
            self._submit_password()

    def _submit_password(self) -> None:
        password = self.query_one("#password-input").value
        logging.debug("Password submitted (length: %d)", len(password))
        self.dismiss(password)