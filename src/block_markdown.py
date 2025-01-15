import re

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    blocks = []
    for block in sections:
        if len(block) == 0:
            continue
        blocks.append(block.strip())

    return blocks

def block_to_block_type(block):
    # check to see if this block is just a heading
    if block.startswith("#"):
        return "heading"

    # check if we start and end with ``` (if we START, but don't end, that is an
    # error)
    if block.startswith("```"):
        if block.endswith("```"):
            return "code"
        else:
            # we just return paragraph
            return "paragraph"

    # split up lines now to check each line has a quote, or list character
    lines = block.split("\n")
    quoted = list(filter(lambda x: x.startswith(">"), lines))
    if len(quoted) == len(lines):
        # we get everything back, meaning they all start with 
        return "quote"

    unordered_star = list(filter(lambda x: x.startswith("* "), lines))
    unordered_dash = list(filter(lambda x: x.startswith("- "), lines))
    if len(lines) == len(unordered_star) or len(lines) == len(unordered_dash) or len(lines) == (len(unordered_star) + len(unordered_dash)):
        return "unordered_list"

    ordered_list = list(map(lambda x: re.findall(r"(\d)\. (.*)", x), lines))
    # check we have the right amount of items (number starts each line followed
    # by . and space)
    if len(lines) != len(ordered_list):
        return "paragraph"
    # check we increment, starting at 1
    cnt = 0
    for item in ordered_list:
        if len(item) == 0:
            return "paragraph"
        if int(item[0][0]) != cnt + 1:
            # didn't increment, paragraph
            return "paragraph"
        cnt += 1

    return "ordered_list"
