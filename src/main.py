from textnode import TextNode, TextType

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