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

# Shown as an 11th, file-less option when more than len(LOGIN_METHODS) txt
# files exist, gently teasing whoever hoarded that many files.
BONUS_ROAST_METHOD = "Log in with ‘I definitely don't have too many text files’"
ROAST_MESSAGE = "✗ Nope. Maybe tidy up texts/ before your next login attempt."


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

    def _real_option_count(self) -> int:
        return min(len(LOGIN_METHODS), len(self._available_files))

    def _has_bonus_option(self) -> bool:
        return len(self._available_files) > len(LOGIN_METHODS)

    def _total_option_count(self) -> int:
        return self._real_option_count() + (1 if self._has_bonus_option() else 0)

    def _render_options(self) -> str:
        real_count = self._real_option_count()
        lines = []
        for i in range(real_count):
            method = LOGIN_METHODS[i]
            filename = self._available_files[i].name
            marker = "❯" if i == self._cursor else " "
            lines.append(f"{marker} {i + 1}. {method} ({filename})")
        if self._has_bonus_option():
            marker = "❯" if self._cursor == real_count else " "
            lines.append(f"{marker} {real_count + 1}. {BONUS_ROAST_METHOD}")
        return "\n".join(lines)

    def action_move_cursor(self, delta: int) -> None:
        if self._logging_in:
            return
        count = self._total_option_count()
        if count == 0:
            return
        self._cursor = (self._cursor + delta) % count
        self.query_one("#login-options", Static).update(self._render_options())

    async def action_select(self) -> None:
        if self._logging_in or self._total_option_count() == 0:
            return
        if self._has_bonus_option() and self._cursor == self._real_option_count():
            await self._select_bonus_roast()
            return
        self._logging_in = True
        selected_path = self._available_files[self._cursor]
        status = self.query_one("#login-status", Static)
        status.update("Logging in...")
        await asyncio.sleep(0.8)
        status.update("✔ Login successful.")
        await asyncio.sleep(0.5)
        self._on_select(selected_path)

    async def _select_bonus_roast(self) -> None:
        self._logging_in = True
        status = self.query_one("#login-status", Static)
        status.update("Logging in...")
        await asyncio.sleep(0.8)
        status.update(ROAST_MESSAGE)
        await asyncio.sleep(1.5)
        status.update("")
        self._logging_in = False
