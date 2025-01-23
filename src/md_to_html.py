from block_markdown import block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import os
import pathlib

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def make_block_node(block, block_type):
    if block_type == "paragraph":
        return paragraph_node(block)
    elif block_type == "heading":
        return heading_node(block)
    elif block_type == "code":
        return code_node(block)
    elif block_type == "quote":
        return quote_node(block)
    elif block_type == "unordered_list":
        return ul_node(block)
    elif block_type == "ordered_list":
        return ol_node(block)
    else:
        raise ValueError("Invalid MD Block")

def paragraph_node(block):
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)

def heading_node(block):
    h_num = 0
    while block.startswith("#"):
        block = block[1:]
        h_num += 1
    return ParentNode(f"h{h_num}", text_to_children(block.strip()))

def code_node(block):
    children = text_to_children(block.strip("```").strip())
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_node(block):
    text = ""
    for line in block.split("\n"):
        text += line.lstrip(">").strip() + " "
    return ParentNode("blockquote", text_to_children(text.strip()))

def ul_node(block):
    list_items = []
    for line in block.split("\n"):
        node = ParentNode("li", text_to_children(line[2:]))
        list_items.append(node)
    return ParentNode("ul", list_items)

def ol_node(block):
    list_items = []
    for line in block.split("\n"):
        text = line[line.index(".") + 2:]
        node = ParentNode("li", text_to_children(text))
        list_items.append(node)
    return ParentNode("ol", list_items)

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    # loop over each block to get the type and child nodes for each block
    for block in blocks:
        block_type = block_to_block_type(block)
        # based on the block type, we will create a ParentNode (and potentially
        # additional parent nodes in the cases of the lists)
        html_nodes.append(make_block_node(block, block_type))

    # return the final node
    return ParentNode("div", html_nodes, None)

def extract_title(markdown):
    h1 = list(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    if len(h1) != 1:
        raise ValueError("No Heading 1 in Markdown, invalid for HTML conversion")
    return h1[0][2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} with {template_path}")
    with open(template_path, "r") as f:
        template = f.read()
    with open(from_path, "r") as f:
        md = f.read()
    html = markdown_to_html(md).to_html()
    title = extract_title(md)
    final = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final)

def generate_page_recursive(content_path, template_path, output_path):
    # create the directory to public_path 
    for item in os.listdir(content_path):
        if os.path.isfile(os.path.join(content_path, item)):
            print(f"Generating {os.path.join(content_path, item)}")
            html_path = os.path.join(output_path, item).replace(".md", ".html")
            generate_page(os.path.join(content_path, item), template_path,
                          html_path)
        else:
            print(f"Recursing into {os.path.join(content_path, item)}")
            generate_page_recursive(os.path.join(content_path, item),
                                    template_path, os.path.join(output_path,
                                                                item))
