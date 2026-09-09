import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

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
        range(1, len(ordered_numbers) + 1)
    ) and len(ordered_numbers) == len(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
