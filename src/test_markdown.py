import unittest
from markdown import extract_title


class TestMarkdown(unittest.TestCase):
    def test_single_line(self):
        markdown = "# Hello there!"
        hope = extract_title(markdown)
        result = "Hello there!"
        self.assertEqual(hope, result)

    def test_extra_spaces(self):
        markdown = "#     Hello there!       "
        hope = extract_title(markdown)
        result = "Hello there!"
        self.assertEqual(hope, result)

    def test_h2(self):
        markdown = "## Hello there!"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_lines(self):
        markdown = """
# Hello there!
some regular line

New line
"""
        hope = extract_title(markdown)
        result = "Hello there!"
        self.assertEqual(hope, result)

    def test_burried_title(self):
        markdown = """
First line is not the title
# Hello there!
some regular line

New line
"""
        hope = extract_title(markdown)
        result = "Hello there!"
        self.assertEqual(hope, result)


if __name__ == "__main__":
    unittest.main()
