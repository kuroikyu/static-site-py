import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_three_blocks(self):
        md = """# This is a heading 

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        result = markdown_to_blocks(md)
        hope = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]

        self.assertListEqual(result, hope)

    def test_one_block(self):
        md = "# This is a heading"
        result = markdown_to_blocks(md)
        hope = ["# This is a heading"]

        self.assertListEqual(result, hope)

    def test_empty_before(self):
        md = """

            # This is a heading"""
        result = markdown_to_blocks(md)
        hope = ["# This is a heading"]

        self.assertListEqual(result, hope)

    def test_empty_after(self):
        md = """# This is a heading


        """
        result = markdown_to_blocks(md)
        hope = ["# This is a heading"]

        self.assertListEqual(result, hope)

    def test_empty_between(self):
        md = """# This is a heading


But this is just some text.
        """
        result = markdown_to_blocks(md)
        hope = ["# This is a heading", "But this is just some text."]

        self.assertListEqual(result, hope)


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_1(self):
        block = "# Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_heading_2(self):
        block = "## Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_heading_3(self):
        block = "### Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_heading_4(self):
        block = "#### Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_heading_5(self):
        block = "##### Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_heading_6(self):
        block = "###### Hi"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.HEADING.value)

    def test_code_small(self):
        block = "```Hi```"
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.CODE.value)

    def test_code_large(self):
        block = """```
        Hi
        ```"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.CODE.value)

    def test_code_large_multiline(self):
        block = """```
        Hi
        this is
        code
        ```"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.CODE.value)

    def test_code_large_multiline_plus_empty_lines(self):
        block = """```
        Hi
        this is
        code

        def test():
            print("hello")
            return 0

        if __name__ == "__main__":
            test()

        ```"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.CODE.value)

    def test_quote_small(self):
        block = """>Hi"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.QUOTE.value)

    def test_quote_large(self):
        block = """> Hi
> testing
>multiline
> Done."""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.QUOTE.value)

    def test_ordered_list_small(self):
        block = """1. Hi"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.ORDERED_LIST.value)

    def test_ordered_list_large(self):
        block = """1. Hi
2. Test
4. Hello """
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.ORDERED_LIST.value)

    def test_unordered_list_small(self):
        block = """- Hi"""
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.UNORDERED_LIST.value)

    def test_unordered_list_large(self):
        block = """* Hi
- Test
- Hello """
        result = block_to_block_type(block)
        self.assertEqual(result.value, BlockType.UNORDERED_LIST.value)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """- Hello
- This is a test
- Using a UL
- See ya
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Hello</li><li>This is a test</li><li>Using a UL</li><li>See ya</li></ul></div>",
        )

    def test_heading(self):
        md = "## Welcomen"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Welcomen</h2></div>",
        )

    def test_blockquotes(self):
        md = """
> This is a quote
> someone wrote
> in a test. What a test!
>
> - Kuroi, fabled writer of tests
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nsomeone wrote\nin a test. What a test!\n\n- Kuroi, fabled writer of tests</blockquote></div>",
        )

    def test_ordered_list(self):
        md = """1. Hello
2. This is a test
3. Using a OL
4. See ya
12. Wrench!
666. The devil has come. Don't be afraid of a period, or two.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Hello</li><li>This is a test</li><li>Using a OL</li><li>See ya</li><li>Wrench!</li><li>The devil has come. Don't be afraid of a period, or two.</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
