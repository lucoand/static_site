from typing import Optional

class HTMLNode:
    def __init__(self, tag=None, value: Optional[str]=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not Implemented!")

    def props_to_html(self):
        retval = ""
        if self.props != None:
            for key in self.props:
                retval += f' {key}="{self.props[key]}"'
        return retval
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

        


