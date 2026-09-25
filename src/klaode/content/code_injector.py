import re
from pathlib import Path

# 在 txt 文件中用 {{code:相对路径}} 标记要插入代码的位置，
# 相对路径基于 snippets 目录解析。
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
    """引用的代码片段文件不存在。"""


def _guess_language(path: Path) -> str:
    return _LANGUAGE_BY_SUFFIX.get(path.suffix, "")


def inject_code(text: str, snippets_dir: Path) -> str:
    """将文本中的 {{code:...}} 占位符替换为对应代码文件内容的 Markdown 代码块。"""

    def _replace(match: re.Match[str]) -> str:
        relative_path = match.group(1).strip()
        snippet_path = snippets_dir / relative_path
        if not snippet_path.is_file():
            raise SnippetNotFoundError(f"未找到代码片段文件: {snippet_path}")
        code = snippet_path.read_text(encoding="utf-8").rstrip("\n")
        language = _guess_language(snippet_path)
        return f"```{language}\n{code}\n```"

    return _CODE_MARKER.sub(_replace, text)
