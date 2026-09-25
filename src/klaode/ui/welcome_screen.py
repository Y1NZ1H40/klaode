from __future__ import annotations

import asyncio
from typing import Callable

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Static

LOGO = r"""
██╗  ██╗██╗      █████╗  ██████╗ ██████╗ ███████╗
██║ ██╔╝██║     ██╔══██╗██╔═══██╗██╔══██╗██╔════╝
█████╔╝ ██║     ███████║██║   ██║██║  ██║█████╗
██╔═██╗ ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
██║  ██╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
""".strip("\n")

LOGIN_OPTIONS = [
    "Log in with browser (recommended)",
    "Log in with API key",
]


class WelcomeScreen(Screen[None]):
    """Startup screen with a mock login flow, shown before entering the chat."""

    BINDINGS = [
        ("up", "move_cursor(-1)", ""),
        ("down", "move_cursor(1)", ""),
        ("enter", "select", ""),
    ]

    def __init__(self, on_continue: Callable[[], None]) -> None:
        super().__init__()
        self._on_continue = on_continue
        self._cursor = 0
        self._logging_in = False

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="welcome-box"):
                yield Static(LOGO, id="logo")
                yield Static("Welcome to Klaode", id="welcome-title")
                yield Static("Select login method:", id="login-prompt")
                yield Static(self._render_options(), id="login-options")
                yield Static("", id="login-status")

    def _render_options(self) -> str:
        lines = []
        for i, option in enumerate(LOGIN_OPTIONS):
            marker = "❯" if i == self._cursor else " "
            lines.append(f"{marker} {i + 1}. {option}")
        return "\n".join(lines)

    def action_move_cursor(self, delta: int) -> None:
        if self._logging_in:
            return
        self._cursor = (self._cursor + delta) % len(LOGIN_OPTIONS)
        self.query_one("#login-options", Static).update(self._render_options())

    async def action_select(self) -> None:
        if self._logging_in:
            return
        self._logging_in = True
        status = self.query_one("#login-status", Static)
        status.update("Logging in...")
        await asyncio.sleep(0.8)
        status.update("✔ Login successful.")
        await asyncio.sleep(0.5)
        self._on_continue()
