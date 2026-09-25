from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Markdown, Static


class MessageBubble(Vertical):
    """A message container styled like a Claude chat bubble."""

    def __init__(self, content: str, *, role: str = "assistant") -> None:
        super().__init__(classes=f"message message-{role}")
        self._content = content
        self._role = role

    def compose(self) -> ComposeResult:
        label = "Klaode" if self._role == "assistant" else "You"
        yield Static(label, classes="message-role")
        yield Markdown(self._content, classes="message-body")
