from __future__ import annotations

import asyncio
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Input, Static

from klaode.content.blocks import split_into_blocks
from klaode.content.code_injector import inject_code
from klaode.content.loader import read_text_file
from klaode.ui.widgets import MessageBlock

REVEAL_DELAY_SECONDS = 0.4

UPDATE_STATUS_TEXT = "✔ Update installed · Restart to update"

MODES = [
    "auto mode on",
    "auto mode off",
    "plan mode on",
]


class ChatScreen(Screen[None]):
    """Main chat window: message log, update status line, input box, mode line."""

    BINDINGS = [("shift+tab", "cycle_mode", "")]

    def __init__(self, text_path: Path, snippets_dir: Path) -> None:
        super().__init__()
        self._text_path = text_path
        self._snippets_dir = snippets_dir
        self._mode_index = 0

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat-log")
        yield Static(UPDATE_STATUS_TEXT, id="update-status")
        yield Input(placeholder="Type a message...", id="chat-input")
        yield Static(self._render_mode(), id="mode-status")

    def _render_mode(self) -> str:
        return f"⏵⏵ {MODES[self._mode_index]} (shift+tab to cycle)"

    def action_cycle_mode(self) -> None:
        self._mode_index = (self._mode_index + 1) % len(MODES)
        self.query_one("#mode-status", Static).update(self._render_mode())

    async def on_mount(self) -> None:
        raw_text = read_text_file(self._text_path)
        processed_text = inject_code(raw_text, self._snippets_dir)
        blocks = split_into_blocks(processed_text)
        self.run_worker(self._reveal_blocks(blocks), exclusive=True)

    async def _reveal_blocks(self, blocks: list[str]) -> None:
        chat_log = self.query_one("#chat-log", VerticalScroll)
        for block in blocks:
            line = MessageBlock(block, role="assistant")
            await chat_log.mount(line)
            chat_log.scroll_end(animate=False)
            await asyncio.sleep(REVEAL_DELAY_SECONDS)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        event.input.clear()
        if not text:
            return
        chat_log = self.query_one("#chat-log", VerticalScroll)
        await chat_log.mount(MessageBlock(text, role="user"))
        chat_log.scroll_end(animate=False)
