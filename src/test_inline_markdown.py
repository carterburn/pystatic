from typing import NoReturn
import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

    def test_extract_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_split_images(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NormalText
        )
        new_nodes = split_nodes_image([node]) 
        expected = [
            TextNode("This is text with an image ", TextType.NormalText),
            TextNode("to boot dev", TextType.ImageText, "https://www.boot.dev"),
            TextNode(" and ", TextType.NormalText),
            TextNode("to youtube", TextType.ImageText,
                     "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.NormalText,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NormalText),
            TextNode("to boot dev", TextType.LinkText, "https://www.boot.dev"),
            TextNode(" and ", TextType.NormalText),
            TextNode("to youtube", TextType.LinkText,
                     "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_at_end(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com)",
                        TextType.NormalText)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.NormalText),
            TextNode("image", TextType.ImageText, "https://i.imgur.com")
        ])

    def test_link_with_followed_text(self):
        node = TextNode("This is text with a link [here](https://x.com) with text that follows", 
                        TextType.NormalText)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.NormalText),
            TextNode("here", TextType.LinkText, "https://x.com"),
            TextNode(" with text that follows", TextType.NormalText)
        ])

    def test_link_alone(self):
        node = TextNode("[link](https://x.com)", TextType.NormalText)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("link", TextType.LinkText, "https://x.com")
        ])

if __name__ == "__main__":
    unittest.main()
