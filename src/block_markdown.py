def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    blocks = []
    for block in sections:
        if len(block) == 0:
            continue
        blocks.append(block.strip())

    return blocks
