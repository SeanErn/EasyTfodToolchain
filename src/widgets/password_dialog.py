# File: widgets/password_dialog.py

import logging
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static

logger = logging.getLogger()

class PasswordDialog(ModalScreen[str]):
    def compose(self):
        logger.debug("Composing PasswordDialog")
        yield Vertical(
            Static("Enter sudo password:", id="password-prompt"),
            Input(password=True, id="password-input"),
            Button("Submit", variant="primary", id="submit-button"),
            id="dialog-container",
        )

    def on_mount(self):
        logger.debug("PasswordDialog mounted")
        self.query_one("#password-input").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-button":
            logger.debug("Submit button pressed in PasswordDialog")
            self._submit_password()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "password-input":
            logger.debug("Password submitted via input in PasswordDialog")
            self._submit_password()

    def _submit_password(self) -> None:
        password = self.query_one("#password-input").value
        logger.debug("Password submitted (length: %d)", len(password))
        self.dismiss(password)