from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Markdown, Static


class MessageBlock(Vertical):
    """A plain-text transcript entry, with no bubble background or border."""

    def __init__(self, content: str, *, role: str = "assistant") -> None:
        super().__init__(classes=f"message message-{role}")
        self._content = content
        self._role = role

    def compose(self) -> ComposeResult:
        if self._role == "user":
            yield Static(f"> {self._content}", classes="message-user-text")
        else:
            yield Markdown(self._content, classes="message-body")
