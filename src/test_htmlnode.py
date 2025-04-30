from htmlnode import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank",})
        props1 = node.props_to_html()
        props2 = node2.props_to_html()
        self.assertEqual(props1, props2)

    def test_props_to_html(self):
        node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank",})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_repr(self):
        node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank",})
        expected = "HTMLNode(tag=None, value=None, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(str(node), expected)

if __name__ == "__main__":
    unittest.main()

