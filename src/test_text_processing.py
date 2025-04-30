import unittest
from text_processing import *

class TestTextProcessing(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ],
        nodes,
        )

    def test_text_to_textnodes_link_before_image(self):
        text = "This text has a [link](url.com) before an ![image](img.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This text has a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "url.com"),
                TextNode(" before an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "img.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_with_just_regular_text(self):
        text = "Regular text with no fancy gubbins"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Regular text with no fancy gubbins", TextType.TEXT),
            ],
            nodes,
        )
