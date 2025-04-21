from textnode import TextNode, TextType, text_node_to_html_node
from utils import copy_static_to_public


def main():
    my_node = TextNode("This is a text node", TextType.BOLD,
                       "https://www.boot.dev")
    print(my_node)

    my_leaf = text_node_to_html_node(my_node)
    print(my_leaf.to_html())

    copy_static_to_public()


main()
