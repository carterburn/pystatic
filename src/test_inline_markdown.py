import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestUtils(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CodeText)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NormalText),
            TextNode("code block", TextType.CodeText),
            TextNode(" word", TextType.NormalText)
        ])

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BoldText)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NormalText),
            TextNode("bold", TextType.BoldText),
            TextNode(" text", TextType.NormalText)
        ])

    def test_italic(self):
        node = TextNode("This is *italic* text", TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ItalicText)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NormalText),
            TextNode("italic", TextType.ItalicText),
            TextNode(" text", TextType.NormalText)
        ])

    def test_skip_img(self):
        node = TextNode("This is an image", TextType.ImageText, "img/img.jpg")
        new_nodes = split_nodes_delimiter([node], "*", TextType.ItalicText)
        self.assertEqual(new_nodes, [
            TextNode("This is an image", TextType.ImageText, "img/img.jpg")
        ])

    # the rest of the tests are from boot.dev as good additional test cases
    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**",
                        TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BoldText)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NormalText),
            TextNode("bolded", TextType.BoldText),
            TextNode(" word and ", TextType.NormalText),
            TextNode("another", TextType.BoldText)
        ])

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**",
                        TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BoldText)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NormalText),
            TextNode("bolded word", TextType.BoldText),
            TextNode(" and ", TextType.NormalText),
            TextNode("another", TextType.BoldText)
        ])

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NormalText)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BoldText)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ItalicText)
        self.assertEqual(new_nodes, [
            TextNode("bold", TextType.BoldText),
            TextNode(" and ", TextType.NormalText),
            TextNode("italic", TextType.ItalicText)
        ])

if __name__ == "__main__":
    unittest.main()
