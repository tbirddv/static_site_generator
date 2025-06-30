class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        if not value and not children and not props:
            raise ValueError("HTMLNode must have either a value, children or attributes.")
        
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        if self.tag and self.value and self.children and self.props :
            return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        elif self.tag and self.value and self.children:
            return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children})"
        elif self.tag and self.value and self.props:
            return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"
        elif self.tag and self.children and self.props:
            return f"HTMLNode(tag={self.tag}, children={self.children}, props={self.props})"
        elif self.tag and self.props:
            return f"HTMLNode(tag={self.tag}, props={self.props})"
        elif self.tag and self.value:
            return f"HTMLNode(tag={self.tag}, value={self.value})"
        elif self.tag and self.children:
            return f"HTMLNode(tag={self.tag}, children={self.children})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if not value:
            raise ValueError("LeafNode must have a value.")
    
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value to convert to HTML.")
        if not self.tag:
            return str(self.value)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
class ImageNode(HTMLNode):
    def __init__(self, tag, props):
        super().__init__(tag=tag, props=props)
        if not self.tag:
            raise ValueError("ImageNode must have a tag")
        if not self.props or "src" not in self.props:
            raise ValueError("ImageNode must have a 'src' property")
        if not isinstance(self.props.get("src"), str):
            raise TypeError("The 'src' property of ImageNode must be a string.")
        if not self.props.get("src"):
            raise ValueError("The 'src' property of ImageNode cannot be empty.")
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ImageNode must have a tag to convert to HTML.")
        if not self.props or "src" not in self.props:
            raise ValueError("ImageNode must have a 'src' property to convert to HTML.")
        if not isinstance(self.props.get("src"), str):
            raise TypeError("The 'src' property of ImageNode must be a string.")
        if not self.props.get("src"):
            raise ValueError("The 'src' property of ImageNode cannot be empty.")
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html} />"
    
    def to_html(self):
        if "src" not in self.props:
            raise ValueError("ImageNode must have a 'src' property to convert to HTML.")
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html} />"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        if not tag:
            raise ValueError("ParentNode must have a tag.")
        if not children:
            raise ValueError("ParentNode must have children.")
        for child in children:
            if not isinstance(child, HTMLNode):
                raise TypeError("All children must be instances of HTMLNode.")
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML.")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML.")
        return f"<{self.tag}{self.props_to_html()}>" + "".join(child.to_html() for child in self.children) + f"</{self.tag}>"