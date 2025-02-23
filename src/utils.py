import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) < 2:
            raise ValueError(
                f"Only one delimiter {delimiter} found in \"{node.text}\". Not valid markdown syntax.")

        text, matched_type, maybe = node.text.split(delimiter, 2)
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

        if len(matched_type) > 0:
            new_nodes.append(TextNode(matched_type, text_type))

        if len(maybe) == 0:
            continue

        if maybe.count(delimiter) > 1:
            new_nodes.extend(split_nodes_delimiter(
                [TextNode(maybe, TextType.TEXT)], delimiter, text_type)
            )
        else:
            new_nodes.append(TextNode(maybe, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    image_regex = r"(?<=!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_regex, text)
    return matches


def extract_markdown_links(text):
    image_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_regex, text)
    return matches


def split_nodes_complex(old_nodes: list[TextNode], text_type: TextType, fn, split_string: str):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        matches = fn(node.text)
        target_text = node.text
        for (label, url) in matches:
            split_by = split_string.replace(
                "{label}", label).replace("{url}", url)
            parts = target_text.split(split_by, 1)
            if len(parts[0]) > 0:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(label, text_type, url))
            target_text = parts[1]
        if len(target_text) > 0:
            result.append(TextNode(target_text, TextType.TEXT))

    return result


def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_complex(old_nodes, TextType.IMAGE, extract_markdown_images, "![{label}]({url})")


def split_nodes_link(old_nodes: list[TextNode]):
    return split_nodes_complex(old_nodes, TextType.LINK, extract_markdown_links, "[{label}]({url})")


