import unittest

from block_markdown import block_to_block_type, markdown_to_blocks

class TestUtils(unittest.TestCase):
    def test_block_split(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_heading_block(self):
        text = "# Heading"
        self.assertEqual("heading", block_to_block_type(text))
        text = "## Heading 2"
        self.assertEqual("heading", block_to_block_type(text))

    def test_code_block(self):
        text = "```python\n\tx = 5\n\ty=10\n\tprint(x+y)\n```"
        self.assertEqual("code", block_to_block_type(text))

    def test_quote_block(self):
        text = "> Quote line 1\n> Quote line 2"
        self.assertEqual("quote", block_to_block_type(text))

    def test_unordered_list(self):
        text = "* List item\n* List item"
        self.assertEqual("unordered_list", block_to_block_type(text))

    def test_ordered_list(self):
        text = "1. List item\n2. List item"
        self.assertEqual("ordered_list", block_to_block_type(text))

    def test_paragraph(self):
        text = "Just a normal paragraph\n"
        self.assertEqual("paragraph", block_to_block_type(text))

if __name__ == "__main__":
    unittest.main()
