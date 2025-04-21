import re
import os
import shutil
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


def text_to_textnodes(text: str):
    node = TextNode(text, TextType.TEXT)
    add_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    add_italic = split_nodes_delimiter(add_bold, "*", TextType.ITALIC)
    add_italic2 = split_nodes_delimiter(add_italic, "_", TextType.ITALIC)
    add_code = split_nodes_delimiter(add_italic2, "`", TextType.CODE)
    add_image = split_nodes_image(add_code)
    add_link = split_nodes_link(add_image)

    return add_link


def copy_static_to_public():
    local_root = "./"
    source_directory = "static"
    target_directory = "public"
    local_target_directory = local_root + target_directory
    local_source_directory = local_root + source_directory

    # Delete and recreate target_directory
    root_directories = os.listdir(local_root)
    if target_directory in root_directories:
        delete_and_recreate_directory(local_target_directory)
    else:
        os.mkdir(local_target_directory)

    # Copy contents of static to target_directory
    copy_directory_to_directory(local_source_directory, local_target_directory)


def delete_and_recreate_directory(target: str):
    shutil.rmtree(target)
    os.mkdir(target)


def ensure_directory_exists(target: str):
    if not os.path.exists(target):
        os.mkdir(target)


def copy_directory_to_directory(source: str, target: str):
    directories = []

    ensure_directory_exists(target)

    for entry in os.listdir(source):
        entry_path = os.path.join(source, entry)
        target_path = os.path.join(target, entry)

        if os.path.isfile(entry_path):
            shutil.copy(entry_path, target_path)

        elif os.path.isdir(entry_path):
            directories.append(entry)

        else:
            print(f"[ERROR]: {entry_path} is not a file, nor a directory.")

    for directory in directories:
        source_path = os.path.join(source, directory)
        target_path = os.path.join(target, directory)
        copy_directory_to_directory(source_path, target_path)
