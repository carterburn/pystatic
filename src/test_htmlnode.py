import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_creation(self):
        node = HTMLNode(tag="a", value="Link Text")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link Text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props(self):
        node = HTMLNode(tag="a", value="Link Text", \
                        props = {"href": "https://www.google.com",  "target": "_blank"})
        output = node.props_to_html()
        self.assertEqual(output, ' href="https://www.google.com" target="_blank"')

    def test_children(self):
        node = HTMLNode(tag="a", value="Link Text")
        para = HTMLNode(tag="p", value="Hello paragraph!", children=[node])
        self.assertEqual(len(para.children), 1)
        self.assertEqual(para.children[0].value, "Link Text")

class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")
