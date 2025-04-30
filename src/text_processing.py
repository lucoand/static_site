from textnode import *
from conversion import *

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = []
    node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_links(text_nodes)
    return text_nodes
