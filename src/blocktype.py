from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_blocktype(block: str) -> BlockType:
    if re.findall(r"^#{1,6} ", block):
        return BlockType.HEADING
    if len(re.findall(r"`{3}", block)) == 2:
        return BlockType.CODE
    lines = block.split("\n")
    length = len(lines)
    x = 0
    for line in lines:
        if re.findall(r"^>", line):
            x += 1
        else:
            break
    if length == x:
        return BlockType.QUOTE
    x = 0
    for line in lines:
        if re.findall(r"^- ", line):
            x += 1
        else:
            break
    if length == x:
        return BlockType.UNORDERED_LIST
    x = 0
    i = 1
    for line in lines:
        if str(i) == line[0] and re.findall(r"^\. ", line[1:]):
            x += 1
            i += 1
        else:
            break
    if length == x:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH





