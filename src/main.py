from textnode import TextNode, TextType, text_node_to_html_node


def main():
    my_node = TextNode("This is a text node", TextType.BOLD,
                       "https://www.boot.dev")
    print(my_node)

    my_leaf = text_node_to_html_node(my_node)
    print(my_leaf.to_html())


main()
