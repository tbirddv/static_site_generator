from enum import Enum
from htmlnode import LeafNode, ImageNode

class TextType(Enum):
    PLAIN = "PLAIN"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        if text_type == TextType.LINK or text_type == TextType.IMAGE:
            if not url:
                raise ValueError(f"{text_type.value} nodes must have a URL.")
        elif url:
            raise ValueError(f"{text_type.value} nodes cannot have a URL.")
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        if self.url:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value})"
    
    def to_html_node(self):
        if self.text_type == TextType.PLAIN:
            return LeafNode(tag=None, value=self.text)
        elif self.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=self.text)
        elif self.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=self.text)
        elif self.text_type == TextType.CODE:
            return LeafNode(tag="code", value=self.text)
        elif self.text_type == TextType.LINK:
            return LeafNode(tag="a", value=self.text, props={"href": self.url})
        elif self.text_type == TextType.IMAGE:
            if not self.text:
                return ImageNode(tag="img", props={"src": self.url})
            return ImageNode(tag="img", props={"src": self.url, "alt": self.text})
        else:
            raise ValueError(f"Unsupported TextType: {self.text_type}")