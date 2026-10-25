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

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_numbers = []
    for line in lines:
        match = re.match(r"^(\d+)\. ", line)
        if not match:
            break
        ordered_numbers.append(int(match.group(1)))
    if ordered_numbers and ordered_numbers == list(
        range(ordered_numbers[0], ordered_numbers[0] + len(ordered_numbers))
    ) and len(ordered_numbers) == len(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
