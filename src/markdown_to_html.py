from conversion import *
from blocktype import BlockType, block_to_blocktype
from text_processing import *
from markdown_to_blocks import *

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    # print(f"{blocks}")
    child_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == BlockType.CODE:    
            code_block_node = TextNode(block[4:-3], TextType.CODE)
            # print(f"{code_block_node}")
            code_block_html_node = text_node_to_html_node(code_block_node)
            code_block_parent_node = ParentNode("pre", [code_block_html_node])
            child_nodes.append(code_block_parent_node)
            continue
        if block_type == BlockType.QUOTE:
            # block = trim_block_signifier(block, "> ")
            # quote_blocks = markdown_to_blocks(block)
            # if len(quote_blocks) == 1:
            #     quote_node = parent_node_generator(quote_blocks[0], "blockquote")
            #     child_nodes.append(quote_node)
            #     continue
            # quote_nodes = []
            # for quote_block in quote_blocks:
            #     quote_node = parent_node_generator(quote_block, "p")
            #     quote_nodes.append(quote_node)
            lines = block.split("\n")
            # print(f"{lines}")
            for i, line in enumerate(lines):
                lines[i] = line[2:]
            # print(f"{lines}")
            block = "\n".join(lines)
            quote_blocks = markdown_to_blocks(block)
            # quote_node = ParentNode("blockquote", quote_nodes)
            quote_block = " ".join(quote_blocks)
            quote_node = parent_node_generator(quote_block, "blockquote")
            child_nodes.append(quote_node)
            continue
        if block_type == BlockType.UNORDERED_LIST:
            block = trim_block_signifier(block, "- ")
            line_list = block.split("\n")
            list_nodes = []
            for line in line_list:
                list_node = parent_node_generator(line, "li")
                list_nodes.append(list_node)
            unordered_node = ParentNode("ul", list_nodes)
            child_nodes.append(unordered_node)
            continue
        if block_type == BlockType.ORDERED_LIST:
            line_list = block.split("\n")
            for i, line in enumerate(line_list):
                line_list[i] = line[3:]
            list_nodes = []
            for line in line_list:
                list_node = parent_node_generator(line, "li")
                list_nodes.append(list_node)
            ordered_node = ParentNode("ol", list_nodes)
            child_nodes.append(ordered_node)
            continue
        if block_type == BlockType.HEADING:
            heading_block = block.split(" ", 1)
            heading_number = len(heading_block[0])
            heading_node = parent_node_generator(heading_block[1], f"h{heading_number}")
            child_nodes.append(heading_node)
            continue
        if block_type == BlockType.PARAGRAPH:
            paragraph_node = parent_node_generator(block, "p")
            child_nodes.append(paragraph_node)
            continue
    parent_html_node = ParentNode("div", child_nodes)
    return parent_html_node

def text_to_children(text: str) -> list[LeafNode]:
    leaf_nodes = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        leaf_node = text_node_to_html_node(node)
        leaf_nodes.append(leaf_node)
    return leaf_nodes

def convert_newlines_to_spaces(children: list[LeafNode]) -> list[LeafNode]:
    for child in children:
        if child.value != None:
            text_list = child.value.split("\n")
            child.value = " ".join(text_list)
    return children

def trim_block_signifier(block: str, signifier: str) -> str:
    return "".join(block.split(signifier))

def parent_node_generator(block: str, tag: str) -> ParentNode:
    block_children = text_to_children(block)
    block_children = convert_newlines_to_spaces(block_children)
    return ParentNode(tag, block_children)
