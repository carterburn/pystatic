import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BoldText)
        node2 = TextNode("This is a text node", TextType.BoldText)
        self.assertEqual(node, node2)

    def test_different_types(self):
        node = TextNode("This is a text node", TextType.BoldText)
        node2 = TextNode("This is a text node", TextType.ItalicText)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BoldText, "http://localhost")
        node2 = TextNode("This is a text node", TextType.BoldText, "http://localhost")
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BoldText, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.BoldText, "http://localhost")
        self.assertNotEqual(node, node2)

    def test_one_url(self):
        node = TextNode("This is a text node", TextType.BoldText, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.BoldText)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is text1", TextType.NormalText)
        node2 = TextNode("This is text2", TextType.NormalText)
        self.assertNotEqual(node, node2)

class TestTextToHTML(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is normal text", TextType.NormalText)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "This is normal text")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BoldText)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ItalicText)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code", TextType.CodeText)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "This is code")

    def test_link(self):
        node = TextNode("This is link text", TextType.LinkText,
                        "https://www.google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "This is link text")
        out = html.to_html()
        self.assertEqual(out, "<a href=\"https://www.google.com\">This is link text</a>")


    def test_image(self):
        node = TextNode("Alt image text", TextType.ImageText, "img/home.jpg")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        out = html.to_html()
        self.assertEqual(out, "<img src=\"img/home.jpg\" alt=\"Alt image text\"></img>")

if __name__ == "__main__":
    unittest.main()
