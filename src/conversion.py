from parentnode import *
from leafnode import *
from textnode import TextType, TextNode
from extract import *

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGES:
        return LeafNode("img", "", {"src": text_node.url,"alt": text_node.text})
    raise Exception("Invald TextType!")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_list = node.text.split(delimiter)
        # print(f"List length = {len(text_list)}")
        # print(f"{text_list}")
        if len(text_list) == 1:
            # print(f"{node}")
            new_nodes.append(node)
            # print(f"{new_nodes}")
            continue
        if (len(text_list) & 1) == 0:
            raise Exception(f"Unmatched delimiter in node: {node.text}")
        if text_list[0] == '' and text_list[2] == '' and len(text_list) == 3:
            new_node = TextNode(text_list[1], text_type)
            new_nodes.append(new_node)
            continue 
        block = 0
        for string in text_list:
            if string == '' and block == 0:
                block = 1
                continue
            if block == 0:
                block = 1
                new_node = TextNode(string, TextType.TEXT)
                new_nodes.append(new_node)
                continue
            if block == 1:
                block = 0
                new_node = TextNode(string, text_type)
                new_nodes.append(new_node)
                continue
        # print(f"retval= {new_nodes}")
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    # pass your nodes through this before split_nodes_links
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        text_list = []
        node_text = node.text
        i = 0
        while i < len(images): 
            temp_list = node_text.split("![", 1)
            text_list.append(temp_list[0])
            temp_list = temp_list[1].split(")", 1)
            text_list.append(temp_list[0])
            node_text = temp_list[1]
            i += 1
        if node_text != "":
            text_list.append(node_text)
        block = 0
        i = 0
        for string in text_list:
            if string == '' and block == 0:
                block = 1
                continue
            if block == 0:
                block = 1
                new_node = TextNode(string, TextType.TEXT)
                new_nodes.append(new_node)
                continue
            if block == 1:
                block = 0
                new_node = TextNode(images[i][0], TextType.IMAGES, images[i][1])
                new_nodes.append(new_node)
                i += 1
                continue
    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    # Run this after images have been extracted
    # if only passed a node with only images and no links, the "links" variable will be empty,
    # but if a node has an image BEFORE a link, it will produce Bad Behavior
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        text_list = []
        node_text = node.text
        i = 0
        while i < len(links): 
            temp_list = node_text.split("[", 1)
            text_list.append(temp_list[0])
            temp_list = temp_list[1].split(")", 1)
            text_list.append(temp_list[0])
            node_text = temp_list[1]
            i += 1
        if node_text != "":
            text_list.append(node_text)
        block = 0
        i = 0
        for string in text_list:
            if string == '' and block == 0:
                block = 1
                continue
            if block == 0:
                block = 1
                new_node = TextNode(string, TextType.TEXT)
                new_nodes.append(new_node)
                continue
            if block == 1:
                block = 0
                new_node = TextNode(links[i][0], TextType.LINKS, links[i][1])
                new_nodes.append(new_node)
                i += 1
                continue
    return new_nodes

