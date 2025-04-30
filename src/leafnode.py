from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode MUST have a value")
        if self.tag == None:
            return str(self.value)
        props = self.props_to_html()
        if self.tag == "img":
            return f'<img{props} />'
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode(tag={self.tag}, value={self.value}, props={self.props})'
