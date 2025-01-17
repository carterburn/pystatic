from block_markdown import block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def strip_block_text(block, block_type):
    if block_type == "paragraph":
        return block
    elif block_type == "heading":
        # need to keep the heading to choose the HTML heading
        return block
    elif block_type == "code":
        return block.strip("```").strip()
    elif block_type == "quote":
        modified = ""
        for line in block.split("\n"):
            modified += line.strip(">").strip() + "\n"
        return modified[:-1]
    elif block_type == "unordered_list":
        # need to only care about lines that start with * or - but not remove
        # other * (could be bold or italic)
        modified = ""
        for line in block.split("\n"):
            modified += line.strip("*").strip("-").strip() + "\n"
        return modified[:-1]
    elif block_type == "ordered_list":
        modified = ""
        for line in block.split("\n"):
            modified += line[line.index(".") + 2:] + "\n"
        return modified[:-1]

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def make_block_node(block, block_type):
    if block_type == "paragraph":
        block = block.replace("\n", " ")
        children = text_to_children(block)
        return ParentNode("p", children, None)
    elif block_type == "heading":
        h_num = 0
        while block.startswith("#"):
            block = block[1:]
            h_num += 1
        text = block.strip()
        return ParentNode(f"h{h_num}", text_to_children(text), None)
    elif block_type == "code":
        code = ParentNode("code", text_to_children(block), None)
        return ParentNode("pre", [code])
    elif block_type == "quote":
        block = block.replace("\n", " ")
        return ParentNode("blockquote", text_to_children(block), None)
    elif block_type == "unordered_list":
        # loop over the lines of the block and create a parent node for each of
        # them with the text as the children
        children = []
        for line in block.split("\n"):
            pnode = ParentNode("li", text_to_children(line), None)
            children.append(pnode)
        return ParentNode("ul", children, None)
    elif block_type == "ordered_list":
        # same as with unordered lists
        children = []
        for line in block.split("\n"):
            pnode = ParentNode("li", text_to_children(line), None)
            children.append(pnode)
        return ParentNode("ol", children, None)

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    # loop over each block to get the type and child nodes for each block
    for block in blocks:
        block_type = block_to_block_type(block)
        modified_text = strip_block_text(block, block_type)
        # based on the block type, we will create a ParentNode (and potentially
        # additional parent nodes in the cases of the lists)
        html_nodes.append(make_block_node(modified_text, block_type))

    # return the final node
    return ParentNode("div", html_nodes, None)
