import re
from pathlib import Path

# Mark where to inject code in a txt file with {{code:relative/path}}.
# The relative path is resolved against the snippets directory.
_CODE_MARKER = re.compile(r"\{\{code:([^}]+)\}\}")

_LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".sh": "bash",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
}


class SnippetNotFoundError(FileNotFoundError):
    """Raised when the referenced snippet file does not exist."""


def _guess_language(path: Path) -> str:
    return _LANGUAGE_BY_SUFFIX.get(path.suffix, "")


def inject_code(text: str, snippets_dir: Path) -> str:
    """Replace {{code:...}} placeholders in text with a fenced Markdown code block."""

    def _replace(match: re.Match[str]) -> str:
        relative_path = match.group(1).strip()
        snippet_path = snippets_dir / relative_path
        if not snippet_path.is_file():
            raise SnippetNotFoundError(f"未找到代码片段文件: {snippet_path}")
        code = snippet_path.read_text(encoding="utf-8").rstrip("\n")
        language = _guess_language(snippet_path)
        return f"```{language}\n{code}\n```"

    return _CODE_MARKER.sub(_replace, text)
