from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # ensure this is a NormalText node
        if node.text_type != TextType.NormalText:
            new_nodes.append(node)
            continue

        # check for an even number of delimiters
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid number of delimiters ({delimiter}) in node: {node.text}")

        split = node.text.split(delimiter)
        # advance by 2 to walk with i = TextNode, i+1 = delimited node
        # i + 1 will not be available on the last one
        for i in range(len(split)):
            if split[i] == "":
                # skip blank strings
                continue
            # add the new NormalText node 
            if i % 2 == 0:
                new_nodes.append(TextNode(split[i], TextType.NormalText))
            else:
                # add the delimited text 
                new_nodes.append(TextNode(split[i], text_type))

    return new_nodes

def split_nodes_bold():
    def inner(old_nodes):
        return split_nodes_delimiter(old_nodes, "**", TextType.BoldText)
    return inner

def split_nodes_italic():
    def inner(old_nodes):
        return split_nodes_delimiter(old_nodes, "*", TextType.ItalicText)
    return inner

def split_nodes_code():
    def inner(old_nodes):
        return split_nodes_delimiter(old_nodes, "`", TextType.CodeText)
    return inner

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    # negative lookbehind moving in hot...says that if the pattern [.*](.*)
    # matches, there can't be a '!' in front (because that would be an image)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    return split_node_image_text_helper(old_nodes, "![{}]({})",
                                 extract_markdown_images, TextType.ImageText)

def split_nodes_link(old_nodes):
    return split_node_image_text_helper(old_nodes, "[{}]({})",
                                        extract_markdown_links, TextType.LinkText)

# generic function for our extraction
def split_node_image_text_helper(old_nodes, format_str, extract_fn, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NormalText:
            new_nodes.append(node)
            continue
        components = extract_fn(node.text)
        if len(components) == 0:
            # nothing to extract, keep node as normal
            new_nodes.append(node)
            continue

        text = node.text
        for comp in components:
            sections = text.split(format_str.format(comp[0], comp[1]), 1)
            pre = sections[0]
            if len(sections) > 1:
                # reset text only if there is more to process
                text = sections[1]
            if len(pre) > 0:
                new_nodes.append(TextNode(pre, TextType.NormalText))
            new_nodes.append(TextNode(comp[0], text_type, comp[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.NormalText))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NormalText)]
    # move through each of our delimited text types and image and links for a
    # final list of nodes
    fns = [split_nodes_bold(), split_nodes_italic(), split_nodes_code(),
           split_nodes_image, split_nodes_link]
    for f in fns:
        nodes = f(nodes)

    return nodes
