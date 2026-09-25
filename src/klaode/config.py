from pathlib import Path

DEFAULT_TEXTS_DIRNAME = "texts"
DEFAULT_SNIPPETS_DIRNAME = "snippets"


def get_texts_dir(base: Path | None = None) -> Path:
    return (base or Path.cwd()) / DEFAULT_TEXTS_DIRNAME


def get_snippets_dir(base: Path | None = None) -> Path:
    return (base or Path.cwd()) / DEFAULT_SNIPPETS_DIRNAME
