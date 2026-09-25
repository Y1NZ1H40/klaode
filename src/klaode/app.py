from __future__ import annotations

from pathlib import Path

from textual.app import App

from klaode.ui.chat_screen import ChatScreen
from klaode.ui.welcome_screen import WelcomeScreen


class KlaodeApp(App[None]):
    """Terminal app that displays txt content in a Claude-like chat window style."""

    CSS_PATH = "ui/theme.tcss"
    TITLE = "klaode"

    def __init__(self, text_path: Path, snippets_dir: Path) -> None:
        super().__init__()
        self._text_path = text_path
        self._snippets_dir = snippets_dir

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen(on_continue=self._enter_chat))

    def _enter_chat(self) -> None:
        self.push_screen(ChatScreen(self._text_path, self._snippets_dir))

    def go_home(self) -> None:
        """Reset back to a fresh login screen, discarding the current chat."""
        while len(self.screen_stack) > 1:
            self.pop_screen()
        self.push_screen(WelcomeScreen(on_continue=self._enter_chat))
