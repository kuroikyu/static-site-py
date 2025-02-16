import unittest

from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code(self):
        nodes = [
            TextNode("Only one `code` element", TextType.TEXT),
        ]
        split = split_nodes_delimiter(nodes, "`", TextType.CODE)

        hopes = [
            TextNode("Only one ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" element", TextType.TEXT),
        ]
        self.assertListEqual(split, hopes)

    def test_single_bold(self):
        nodes = [
            TextNode("**Bold** text", TextType.TEXT),
        ]
        split = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        hopes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(split, hopes)

    def test_single_itallic(self):
        nodes = [
            TextNode("I love _Italy_", TextType.TEXT),
        ]
        split = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        hopes = [
            TextNode("I love ", TextType.TEXT),
            TextNode("Italy", TextType.ITALIC),
        ]
        self.assertListEqual(split, hopes)

    def test_chained_tags(self):
        nodes = [
            TextNode("This is `code` and this is *bold*", TextType.TEXT),
        ]
        split = split_nodes_delimiter(nodes, "`", TextType.CODE)
        split = split_nodes_delimiter(split, "*", TextType.BOLD)

        hopes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        self.assertListEqual(split, hopes)

    def test_multiple_scenarios(self):
        nodes = [
            TextNode("Hello there", TextType.BOLD),
            TextNode(
                "Let's try this with `code formatting` between `the` `text", TextType.TEXT),
            TextNode("text highlighted in itallics", TextType.ITALIC),
            TextNode("It's a feint`` noise `coming form this direction",
                     TextType.TEXT),
            TextNode("Only one code quote", TextType.TEXT),
            TextNode("No delimiter!", TextType.TEXT),
        ]
        split = split_nodes_delimiter(nodes, "`", TextType.CODE)

        hopes = [
            TextNode("Hello there", TextType.BOLD),
            TextNode(
                "Let's try this with ", TextType.TEXT),
            TextNode(
                "code formatting", TextType.CODE),
            TextNode(
                " between ", TextType.TEXT),
            TextNode(
                "the", TextType.CODE),
            TextNode(
                " `text", TextType.TEXT),
            TextNode("text highlighted in itallics", TextType.ITALIC),
            TextNode("It's a feint", TextType.TEXT),
            TextNode(" noise `coming form this direction", TextType.TEXT),
            TextNode("Only one code quote", TextType.TEXT),
            TextNode("No delimiter!", TextType.TEXT),
        ]
        self.assertListEqual(split, hopes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        md = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        test = extract_markdown_images(md)
        self.assertEqual(
            test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_multiple_images(self):
        md = "Take a look at ![rick roll](https://i.imgur.com/aKaOqIh.gif), an image. Here's another ![test!](image)."
        test = extract_markdown_images(md)
        self.assertEqual(
            test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("test!", "image")])

    def test_single_link(self):
        md = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        test = extract_markdown_images(md)
        self.assertEqual(test, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        md = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        test = extract_markdown_links(md)
        self.assertEqual(
            test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_multiple_links(self):
        md = "Take a look at [rick roll](https://i.imgur.com/aKaOqIh.gif), a link. Here's another [test!](http)."
        test = extract_markdown_links(md)
        self.assertEqual(
            test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("test!", "http")])

    def test_single_image(self):
        md = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        test = extract_markdown_links(md)
        self.assertEqual(test, [])


if __name__ == "__main__":
    unittest.main()
