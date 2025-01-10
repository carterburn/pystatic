from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NormalText = "normal"
    BoldText = "bold"
    ItalicText = "italic"
    CodeText = "code"
    LinkText = "link"
    ImageText = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    if text_type == TextType.NormalText:
        return LeafNode(None, text_node.text)
    if text_type == TextType.BoldText:
        return LeafNode("b", text_node.text)
    if text_type == TextType.ItalicText:
        return LeafNode("i", text_node.text)
    if text_type == TextType.CodeText:
        return LeafNode("code", text_node.text)
    if text_type == TextType.LinkText:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_type == TextType.ImageText:
        return LeafNode("img", "", {"src": text_node.url, "alt":
                                        text_node.text})
    raise ValueError(f"Invalid text type: {text_type}")
