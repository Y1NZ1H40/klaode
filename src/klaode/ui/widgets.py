from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Markdown, Static


class MessageBubble(Vertical):
    """模仿 Claude 对话气泡样式的消息容器。"""

    def __init__(self, content: str, *, role: str = "assistant") -> None:
        super().__init__(classes=f"message message-{role}")
        self._content = content
        self._role = role

    def compose(self) -> ComposeResult:
        label = "Klaode" if self._role == "assistant" else "You"
        yield Static(label, classes="message-role")
        yield Markdown(self._content, classes="message-body")
