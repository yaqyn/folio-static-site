import re


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split blank-line blocks while keeping fenced code, including blank lines."""
    blocks, current = [], []
    fenced = False
    for line in markdown.splitlines():
        if re.fullmatch(r"```[\w+-]*", line.strip()):
            if not fenced:
                if current:
                    blocks.append("\n".join(current).strip())
                    current = []
                fenced = True
                current.append(line.strip())
            elif line.strip() == "```":
                current.append("```")
                blocks.append("\n".join(current))
                current = []
                fenced = False
            else:
                current.append(line)
        elif not line.strip() and not fenced:
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)
    if fenced:
        raise ValueError("Unclosed fenced code block")
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block]
