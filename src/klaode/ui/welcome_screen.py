from __future__ import annotations

import asyncio
from pathlib import Path
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

# Up to 10 login methods can be shown. Each displayed method is paired
# with one discovered txt file, in order, so selecting a method opens
# that specific file.
LOGIN_METHODS = [
    "Log in with browser (recommended)",
    "Log in with API key",
    "Log in with Anthropic Console account",
    "Log in with Claude.ai account",
    "Log in with Google account",
    "Log in with GitHub account",
    "Log in with Okta SSO",
    "Log in with SAML SSO",
    "Log in with AWS Bedrock credentials",
    "Log in with Google Vertex AI credentials",
]


class WelcomeScreen(Screen[None]):
    """Startup screen with a mock login flow.

    Each login method corresponds to one available txt file; selecting a
    method opens its file.
    """

    BINDINGS = [
        ("up", "move_cursor(-1)", ""),
        ("down", "move_cursor(1)", ""),
        ("enter", "select", ""),
    ]

    def __init__(self, available_files: list[Path], on_select: Callable[[Path], None]) -> None:
        super().__init__()
        self._available_files = available_files
        self._on_select = on_select
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

    def _option_count(self) -> int:
        return min(len(LOGIN_METHODS), len(self._available_files))

    def _render_options(self) -> str:
        lines = []
        for i in range(self._option_count()):
            method = LOGIN_METHODS[i]
            filename = self._available_files[i].name
            marker = "❯" if i == self._cursor else " "
            lines.append(f"{marker} {i + 1}. {method} ({filename})")
        return "\n".join(lines)

    def action_move_cursor(self, delta: int) -> None:
        if self._logging_in:
            return
        count = self._option_count()
        if count == 0:
            return
        self._cursor = (self._cursor + delta) % count
        self.query_one("#login-options", Static).update(self._render_options())

    async def action_select(self) -> None:
        if self._logging_in or self._option_count() == 0:
            return
        self._logging_in = True
        selected_path = self._available_files[self._cursor]
        status = self.query_one("#login-status", Static)
        status.update("Logging in...")
        await asyncio.sleep(0.8)
        status.update("✔ Login successful.")
        await asyncio.sleep(0.5)
        self._on_select(selected_path)
