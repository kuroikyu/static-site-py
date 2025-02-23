import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType


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


if __name__ == "__main__":
    unittest.main()
