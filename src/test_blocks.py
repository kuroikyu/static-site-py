import unittest
from blocks import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
