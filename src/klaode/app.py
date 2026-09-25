from __future__ import annotations

import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header

from klaode.content.blocks import split_into_blocks
from klaode.content.code_injector import inject_code
from klaode.content.loader import read_text_file
from klaode.ui.widgets import MessageBubble

REVEAL_DELAY_SECONDS = 0.4


class KlaodeApp(App[None]):
    """Terminal app that displays txt content in a Claude-like chat window style."""

    CSS_PATH = "ui/theme.tcss"
    TITLE = "klaode"
    BINDINGS = [("q", "quit", "退出")]

    def __init__(self, text_path: Path, snippets_dir: Path) -> None:
        super().__init__()
        self._text_path = text_path
        self._snippets_dir = snippets_dir

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="chat-log")
        yield Footer()

    async def on_mount(self) -> None:
        raw_text = read_text_file(self._text_path)
        processed_text = inject_code(raw_text, self._snippets_dir)
        blocks = split_into_blocks(processed_text)
        self.run_worker(self._reveal_blocks(blocks), exclusive=True)

    async def _reveal_blocks(self, blocks: list[str]) -> None:
        chat_log = self.query_one("#chat-log", VerticalScroll)
        for block in blocks:
            bubble = MessageBubble(block, role="assistant")
            await chat_log.mount(bubble)
            chat_log.scroll_end(animate=False)
            await asyncio.sleep(REVEAL_DELAY_SECONDS)
