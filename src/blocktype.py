import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    THEMATIC_BREAK = "thematic_break"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if re.match(r"^```[\w+-]*\n", block) and block.endswith("\n```"):
        return BlockType.CODE

    if re.fullmatch(r" {0,3}((\*[ \t]*){3,}|(-[ \t]*){3,}|(_[ \t]*){3,})", block):
        return BlockType.THEMATIC_BREAK

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(len(line) >= 2 and line[:2] in {"- ", "* ", "+ "} for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_numbers = []
    for line in lines:
        match = re.match(r"^(\d+)([.)]) ", line)
        if not match:
            break
        ordered_numbers.append((int(match.group(1)), match.group(2)))
    if ordered_numbers and len(ordered_numbers) == len(lines):
        numbers = [number for number, _ in ordered_numbers]
        delimiters = {delimiter for _, delimiter in ordered_numbers}
        if len(delimiters) == 1 and numbers == list(
            range(numbers[0], numbers[0] + len(numbers))
        ):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
