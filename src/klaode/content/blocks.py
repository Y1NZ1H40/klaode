def split_into_blocks(text: str) -> list[str]:
    """Split text into display blocks on blank lines, keeping fenced code blocks intact."""
    lines = text.splitlines()
    blocks: list[str] = []
    buffer: list[str] = []
    in_code_block = False

    def flush() -> None:
        if buffer:
            block = "\n".join(buffer).strip("\n")
            if block:
                blocks.append(block)
            buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code_block:
                flush()
                buffer.append(line)
                in_code_block = True
            else:
                buffer.append(line)
                flush()
                in_code_block = False
            continue

        if in_code_block:
            buffer.append(line)
            continue

        if stripped == "":
            flush()
            continue

        buffer.append(line)

    flush()
    return blocks
