from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"
    TEXT = "text"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
