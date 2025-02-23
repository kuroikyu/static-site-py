def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            result.append(block)
    return result
