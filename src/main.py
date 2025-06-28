from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode, ImageNode

def text_node_to_leaf_node(text_node: TextNode):
    """
    Converts a TextNode to a LeafNode.
    """
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.text:
            return ImageNode(tag="img", props={"src": text_node.url})
        return ImageNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def main():
    test_node = TextNode("Hello, World!", TextType.PLAIN)
    test_node_bold = TextNode("Bold Text", TextType.BOLD)
    test_node_italic = TextNode("Italic Text", TextType.ITALIC)
    test_node_code = TextNode("Code Snippet", TextType.CODE)
    test_node_image = TextNode("Image Description", TextType.IMAGE, "https://example.com/image.png")
    test_link_node = TextNode("OpenAI", TextType.LINK, "https://www.openai.com")
    print(test_node)
    print(test_node_bold)
    print(test_node_italic)
    print(test_node_code)
    print(test_node_image)
    print(test_link_node)

if __name__ == "__main__":
    main()