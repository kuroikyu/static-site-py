import unittest

from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes
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


class TestSplitNodesImage(unittest.TestCase):
    def test_integrated_image(self):
        node = TextNode("This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) hi",
                        TextType.TEXT)
        result = split_nodes_image([node])
        hope = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE,
                     "https://www.youtube.com/@bootdotdev"),
            TextNode(" hi", TextType.TEXT),
        ]

        self.assertListEqual(result, hope)

    def test_integrated_link(self):
        node = TextNode("This is text with an image ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) bye",
                        TextType.TEXT)
        result = split_nodes_image([node])
        hope = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(
                " and [to youtube](https://www.youtube.com/@bootdotdev) bye", TextType.TEXT),
        ]

        self.assertListEqual(result, hope)


class TestSplitNodesLink(unittest.TestCase):
    def test_integrated_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) bye",
                        TextType.TEXT)
        result = split_nodes_link([node])
        hope = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK,
                     "https://www.youtube.com/@bootdotdev"),
            TextNode(" bye", TextType.TEXT),
        ]

        self.assertListEqual(result, hope)

    def test_integrated_link(self):
        node = TextNode("This is text with an image [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) hi",
                        TextType.TEXT)
        result = split_nodes_image([node])
        hope = [
            TextNode(
                "This is text with an image [to boot dev](https://www.boot.dev) and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE,
                     "https://www.youtube.com/@bootdotdev"),
            TextNode(" hi", TextType.TEXT),
        ]

        self.assertListEqual(result, hope)


class TestTextToTextnodes(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        hope = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(result, hope)


if __name__ == "__main__":
    unittest.main()
