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
