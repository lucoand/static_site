from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node must be passed a tag!")
        if self.children == None:
            raise ValueError("Parent Node must contain a child/children!")
        props = self.props_to_html()
        children = ""
        # print(f"{self.children}")
        for child in self.children:
            children += child.to_html()
        return f'<{self.tag}{props}>{children}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode(tag={self.tag}, children={self.children}, props={self.props})'
