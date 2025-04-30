def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    raw_blocks = markdown.split("\n\n")
    raw_blocks = [x for x in raw_blocks if x != ""]
    for block in raw_blocks:
        blocks.append(block.strip())
    return blocks
