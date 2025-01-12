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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    # negative lookbehind moving in hot...says that if the pattern [.*](.*)
    # matches, there can't be a '!' in front (because that would be an image)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
