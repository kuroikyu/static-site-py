import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node1 = TextNode("A test", TextType.ITALIC, "https://example.com")
        node2 = TextNode("This won't match", TextType.ITALIC,
                         "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_text_type(self):
        node1 = TextNode("A test", TextType.ITALIC, "https://example.com")
        node2 = TextNode("A test", TextType.CODE, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("A test", TextType.TEXT, "https://example.com")
        node2 = TextNode("A test", TextType.TEXT)
        self.assertNotEqual(node1, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("A node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "A node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://img.src")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "http://img.src", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("BOOOOLD", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "BOOOOLD")


if __name__ == "__main__":
    unittest.main()
