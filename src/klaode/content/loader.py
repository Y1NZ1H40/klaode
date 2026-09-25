from pathlib import Path


def list_text_files(texts_dir: Path) -> list[Path]:
    """列出目录下所有 .txt 文件，按文件名排序。"""
    if not texts_dir.exists():
        return []
    return sorted(p for p in texts_dir.glob("*.txt") if p.is_file())


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")
