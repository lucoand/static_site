import unittest
from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("b", "grandchild",{"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b href="https://www.google.com">grandchild</b></span></div>',
        )

    def test_to_html_multiple_grandchildren_and_child_props(self):
        grandchild1_node = LeafNode("b", "grandchild1")
        grandchild2_node = LeafNode("i", "grandchild2")
        grandchild3_node = LeafNode(None, "grandchild3")
        child_node = ParentNode("p", [grandchild1_node, grandchild2_node, grandchild3_node], {"property": "value", "other": "other value"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><p property="value" other="other value"><b>grandchild1</b><i>grandchild2</i>grandchild3</p></div>'
        )

    def test_to_html_multiple_children_with_grandchildren_and_parent_props(self):
        grandchild1_node = LeafNode("b", "grandchild1")
        grandchild2_node = LeafNode("i", "grandchild2")
        child_node = ParentNode("h1", [grandchild1_node])
        sibling_node = ParentNode("p", [grandchild2_node])
        parent_node = ParentNode("div", [child_node, sibling_node], {"href": "boot.dev"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="boot.dev"><h1><b>grandchild1</b></h1><p><i>grandchild2</i></p></div>'
        )
