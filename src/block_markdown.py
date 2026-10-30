import re


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split blank-line blocks while keeping fenced code, including blank lines."""
    blocks, current = [], []
    fence = None
    for line in markdown.splitlines():
        fence_match = re.fullmatch(r"(```|~~~)[ \t]*[\w+-]*[ \t]*", line.strip())
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                if current:
                    blocks.append("\n".join(current).strip())
                    current = []
                fence = marker
                current.append(line.strip())
            elif line.strip() == fence:
                current.append(fence)
                blocks.append("\n".join(current))
                current = []
                fence = None
            else:
                current.append(line)
        elif not line.strip() and fence is None:
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)
    if fence is not None:
        raise ValueError("Unclosed fenced code block")
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block]
