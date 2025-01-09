import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()
