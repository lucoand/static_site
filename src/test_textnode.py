import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.IMAGES, None)
        node2 = TextNode("This is a text node", TextType.IMAGES, None)
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.IMAGES, None)
        node2 = TextNode("This is a text node", TextType.IMAGES, 'None')
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINKS)
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a different text node", TextType.CODE)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
