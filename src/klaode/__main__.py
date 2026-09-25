from __future__ import annotations

import argparse
from pathlib import Path

from klaode.app import KlaodeApp
from klaode.config import get_snippets_dir, get_texts_dir
from klaode.content.loader import list_text_files


def _resolve_available_files(file_arg: str | None, texts_dir: Path) -> list[Path]:
    """Resolve the list of txt files offered as login methods on the welcome screen.

    An explicit file argument bypasses the picker entirely (a single option).
    Otherwise every txt file found in texts_dir is returned uncapped; the
    welcome screen itself decides how many real options to show and whether
    to add its bonus "too many files" option.
    """
    if file_arg is not None:
        candidate = Path(file_arg)
        if not candidate.is_absolute():
            candidate = texts_dir / candidate
        if not candidate.is_file():
            raise SystemExit(f"找不到文本文件: {candidate}")
        return [candidate]

    available = list_text_files(texts_dir)
    if not available:
        raise SystemExit(
            f"'{texts_dir}' 目录下没有找到任何 .txt 文件，请先放入文件再运行。"
        )
    return available


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="klaode",
        description="以类 Claude 对话窗口样式在终端中展示 txt 文本内容",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="要展示的 txt 文件名（相对于 texts/ 目录）或绝对路径",
    )
    parser.add_argument(
        "--texts-dir",
        type=Path,
        default=None,
        help="txt 文件所在目录（默认为当前目录下的 texts/）",
    )
    parser.add_argument(
        "--snippets-dir",
        type=Path,
        default=None,
        help="用于注入的代码片段所在目录（默认为当前目录下的 snippets/）",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    texts_dir = args.texts_dir or get_texts_dir()
    snippets_dir = args.snippets_dir or get_snippets_dir()

    available_files = _resolve_available_files(args.file, texts_dir)

    app = KlaodeApp(available_files=available_files, snippets_dir=snippets_dir)
    app.run()


if __name__ == "__main__":
    main()
