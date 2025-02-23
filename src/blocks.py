from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            result.append(block)
    return result


def block_to_block_type(block: str):
    lines = block.split("\n")
    first_line = lines[0]
    last_line = lines[-1]

    # Heading
    if re.search(r"^#{1,6}\s", first_line):
        return BlockType.HEADING

    # Code
    if re.search(r"^`{3}", first_line) and re.search(r"`{3}$", last_line):
        return BlockType.CODE

    # Quote
    quotes = []
    for line in lines:
        if re.search(r"^>", line):
            quotes.append(line)
    if len(lines) == len(quotes):
        return BlockType.QUOTE

    # Unordered list
    uls = []
    for line in lines:
        if re.search(r"^(\*|-)\s", line):
            uls.append(line)
    if len(lines) == len(uls):
        return BlockType.UNORDERED_LIST

    # Ordered list
    ols = []
    for line in lines:
        if re.search(r"^\d*\.\s", line):
            ols.append(line)
    if len(lines) == len(ols):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
