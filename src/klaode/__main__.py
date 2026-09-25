from __future__ import annotations

import argparse
from pathlib import Path

from klaode.app import KlaodeApp
from klaode.config import get_snippets_dir, get_texts_dir
from klaode.content.loader import list_text_files


def _resolve_text_path(file_arg: str | None, texts_dir: Path) -> Path:
    if file_arg is not None:
        candidate = Path(file_arg)
        if not candidate.is_absolute():
            candidate = texts_dir / candidate
        if not candidate.is_file():
            raise SystemExit(f"找不到文本文件: {candidate}")
        return candidate

    available = list_text_files(texts_dir)
    if not available:
        raise SystemExit(
            f"'{texts_dir}' 目录下没有找到任何 .txt 文件，请先放入文件再运行。"
        )
    if len(available) > 1:
        names = ", ".join(p.name for p in available)
        raise SystemExit(
            f"'{texts_dir}' 目录下有多个 txt 文件（{names}），"
            f"请通过参数指定要打开的文件，例如: klaode {available[0].name}"
        )
    return available[0]


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

    text_path = _resolve_text_path(args.file, texts_dir)

    app = KlaodeApp(text_path=text_path, snippets_dir=snippets_dir)
    app.run()


if __name__ == "__main__":
    main()
