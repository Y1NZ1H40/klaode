from klaode.content.blocks import split_into_blocks


def test_split_into_blocks_separates_paragraphs() -> None:
    text = "第一段。\n\n第二段。"

    assert split_into_blocks(text) == ["第一段。", "第二段。"]


def test_split_into_blocks_keeps_fenced_code_block_intact() -> None:
    text = "说明文字\n\n```python\nprint(1)\n```\n\n结尾文字"

    result = split_into_blocks(text)

    assert result == [
        "说明文字",
        "```python\nprint(1)\n```",
        "结尾文字",
    ]
