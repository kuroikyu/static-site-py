from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from utils import text_to_textnodes
from textnode import text_node_to_html_node


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


def strip_md_type_from_block(block, block_type):
    match(block_type):
        case BlockType.CODE:
            return (block[4:-3], None)
        case BlockType.HEADING:
            header_len = len(block.split()[0])
            return (block[header_len+1:], header_len)
        case BlockType.QUOTE | BlockType.UNORDERED_LIST:
            return ("\n".join(map(lambda x: x[2:], block.split("\n"))), None)
        case BlockType.ORDERED_LIST:
            return ("\n".join(map(lambda x: re.split(r"^\d+\.\s", x, maxsplit=1)[1], block.split("\n"))), None)
        case _:
            return (block, None)


def block_body_to_html(block):
    return "".join(map(lambda x: text_node_to_html_node(x).to_html(), text_to_textnodes(block)))


def suround_block_with_html(block, block_type):
    clean_block, header_level = strip_md_type_from_block(block, block_type)
    match(block_type):
        case BlockType.PARAGRAPH:
            return HTMLNode(tag="p", value=block_body_to_html(" ".join(clean_block.split("\n"))))
        case BlockType.CODE:
            return ParentNode(tag="pre", children=HTMLNode(tag="code", value=clean_block))
        case BlockType.HEADING:
            return HTMLNode(tag="h" + str(header_level), value=block_body_to_html(clean_block))
        case BlockType.QUOTE:
            return HTMLNode(tag="blockquote", value=block_body_to_html(clean_block))
        case BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=HTMLNode(tag="li", value="</li><li>".join(block_body_to_html(clean_block).split("\n"))))
        case BlockType.ORDERED_LIST:
            return ParentNode(tag="ol", children=HTMLNode(tag="li", value="</li><li>".join(block_body_to_html(clean_block).split("\n"))))


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    result = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        html_block = suround_block_with_html(block, block_type)
        result.append("".join(html_block.to_html()))
    return ParentNode(tag="div", children="".join(result))
