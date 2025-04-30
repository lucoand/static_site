import unittest
from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_multi_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "key": "value"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" key="value">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text!!")
        self.assertEqual(node.to_html(), "<b>Bold text!!</b>")

    def test_leaf_to_html_long_tag(self):
        node = LeafNode("article", "Weather forecast", {"class": "forecast"})
        self.assertEqual(node.to_html(), '<article class="forecast">Weather forecast</article>')

if __name__ == "__main__":
    unittest.main()
