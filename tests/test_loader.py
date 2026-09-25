from pathlib import Path

from klaode.content.loader import list_text_files, read_text_file


def test_list_text_files_returns_sorted_txt_files(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "note.md").write_text("not txt")

    result = list_text_files(tmp_path)

    assert [p.name for p in result] == ["a.txt", "b.txt"]


def test_list_text_files_missing_dir_returns_empty(tmp_path: Path) -> None:
    assert list_text_files(tmp_path / "missing") == []


def test_read_text_file_reads_utf8_content(tmp_path: Path) -> None:
    path = tmp_path / "hello.txt"
    path.write_text("你好", encoding="utf-8")

    assert read_text_file(path) == "你好"
