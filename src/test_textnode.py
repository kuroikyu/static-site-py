import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
