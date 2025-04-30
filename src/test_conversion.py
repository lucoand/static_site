from contextlib import contextmanager
import unittest
from conversion import *

class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINKS, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGES, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "This is a text node"})

    def test_exception(self):
        bad_node = TextNode(None, text_type="invalid") # this is supposed to be wrong!  ignore lsp
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(bad_node)
        self.assertEqual(str(context.exception), "Invald TextType!")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_no_blocks(self):
        # print(f"Testing no blocks!")
        node = TextNode("This is text with no blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("This is text with no blocks", TextType.TEXT)]
        # print(f"new_nodes= {new_nodes}")
        # print(f"expected = {expected_nodes}")
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_one_big_block(self):
        # print(f"Testing big block!")
        node = TextNode("**This is one big bold block!**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("This is one big bold block!", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_bookended_blocks(self):
        node = TextNode("`starting code block` regular text `ending code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("starting code block", TextType.CODE),
            TextNode(" regular text ", TextType.TEXT),
            TextNode("ending code block", TextType.CODE),
             ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_starting_block_with_back_to_back(self):
        node = TextNode("`starting code block` regular text `second code block``back to back code block` regular text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("starting code block", TextType.CODE),
            TextNode(" regular text ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode("back to back code block", TextType.CODE),
            TextNode(" regular text", TextType.TEXT),
             ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_exception(self):
        bad_node = TextNode("block with 1 (one) ` backtick",TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([bad_node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Unmatched delimiter in node: block with 1 (one) ` backtick")

    def test_split_nodes_multiple_nodes(self):
        nodes = [
                TextNode("regular block", TextType.TEXT),
                TextNode("block with _italics_", TextType.TEXT),
                TextNode("regular block 2", TextType.TEXT),
                TextNode("another _block_ with _multiple_ italics", TextType.TEXT),
                TextNode("regular block 3", TextType.TEXT),
                TextNode("this block shouldn't get messed with", TextType.LINKS),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected_nodes = [
                TextNode("regular block", TextType.TEXT),
                TextNode("block with ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode("regular block 2", TextType.TEXT),
                TextNode("another ", TextType.TEXT),
                TextNode("block", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("multiple", TextType.ITALIC),
                TextNode(" italics", TextType.TEXT),
                TextNode("regular block 3", TextType.TEXT),
                TextNode("this block shouldn't get messed with", TextType.LINKS),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_at_beginning_with_a_link(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) but also a [link](boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" but also a [link](boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_no_images(self):
        node = TextNode( "this is just text!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [ TextNode( "this is just text!", TextType.TEXT) ],
            new_nodes,
        )
        
    def test_split_nodes_image_with_just_an_image_tag(self):
        node = TextNode( "![image](path_to_image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual( [ TextNode("image", TextType.IMAGES, "path_to_image.png"), ], new_nodes)

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("This node has a [link](url) and an ![image](image.png)", TextType.TEXT),
            TextNode("This node is just text.", TextType.TEXT),
            TextNode("![just an image](url.com/image.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("This node has a [link](url) and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "image.png"),
            TextNode("This node is just text.", TextType.TEXT),
            TextNode("just an image", TextType.IMAGES, "url.com/image.png"),
        ], new_nodes)

    def test_split_nodes_image_back_to_back(self):
        node = TextNode("This node has back to back images ![image1](img1.png)![image2](img2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This node has back to back images ", TextType.TEXT),
                TextNode("image1", TextType.IMAGES, "img1.png"),
                TextNode("image2", TextType.IMAGES, "img2.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode("This node has two links! [link1](url1.com) [link2](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This node has two links! ", TextType.TEXT),
                TextNode("link1", TextType.LINKS, "url1.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("link2", TextType.LINKS, "url2.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_links_no_links(self):
        node = TextNode("This is just text!", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([TextNode("This is just text!", TextType.TEXT)], new_nodes)

    def test_split_nodes_links_with_images_like_you_are_not_supposed_to_do(self):
        node = TextNode("This text contains an ![image](url.com/img.png) and isn't supposed to be run through this!", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode("This text contains an ![image](url.com/img.png) and isn't supposed to be run through this!", TextType.TEXT)
            ],
            new_nodes,
        )
            
    def test_split_nodes_images_followed_by_links(self):
        node = TextNode("This text contains an ![image](url.com/img.png) and a [link](boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_links(new_nodes)
        self.assertListEqual(
            [
                TextNode("This text contains an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "url.com/img.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_links_back_to_back_and_multiple_nodes(self):
        nodes = [
            TextNode("This text has back to back links [link1](url1.com)[link2](url2.com)", TextType.TEXT),
            TextNode("image already processed", TextType.IMAGES, "img.png"),
            TextNode("code block", TextType.CODE),
            TextNode("another [link](url3.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("This text has back to back links ", TextType.TEXT),
                TextNode("link1", TextType.LINKS, "url1.com"),
                TextNode("link2", TextType.LINKS, "url2.com"),
                TextNode("image already processed", TextType.IMAGES, "img.png"),
                TextNode("code block", TextType.CODE),
                TextNode("another ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "url3.com"),
            ],
            new_nodes,
        )
    def test_split_nodes_images_with_non_text_nodes(self):
        nodes = [
            TextNode("This text has back to back links [link1](url1.com)[link2](url2.com)", TextType.TEXT),
            TextNode("image already processed", TextType.IMAGES, "img.png"),
            TextNode("code block", TextType.CODE),
            TextNode("an ![image](url3.com/img2.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This text has back to back links [link1](url1.com)[link2](url2.com)", TextType.TEXT),
                TextNode("image already processed", TextType.IMAGES, "img.png"),
                TextNode("code block", TextType.CODE),
                TextNode("an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "url3.com/img2.png"),
            ],
            new_nodes,
        )
