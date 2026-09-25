from pathlib import Path

import pytest

from klaode.content.code_injector import SnippetNotFoundError, inject_code


def test_inject_code_replaces_marker_with_fenced_code_block(tmp_path: Path) -> None:
    snippet = tmp_path / "example.py"
    snippet.write_text("print('hi')\n", encoding="utf-8")

    text = "看看这段代码：\n\n{{code:example.py}}\n\n应该没问题。"
    result = inject_code(text, tmp_path)

    assert "```python\nprint('hi')\n```" in result


def test_inject_code_missing_snippet_raises(tmp_path: Path) -> None:
    text = "{{code:missing.py}}"

    with pytest.raises(SnippetNotFoundError):
        inject_code(text, tmp_path)
