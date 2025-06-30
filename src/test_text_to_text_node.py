import unittest
from textnode import TextNode, TextType
from blocknode import BlockNode, BlockType
from main import markdown_to_blocks

class TestTextToTextNode(unittest.TestCase):
    def test_plain_text(self):
        text = "Hello, World!"
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [TextNode("Hello, World!", TextType.PLAIN)]
        self.assertEqual(nodes, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_italic_text(self):
        text = "This is _italic_ text."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_code_text(self):
        text = "This is `code` text."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_link_text(self):
        text = "This is a [link](https://example.com)."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_image_text(self):
        text = "This is an ![image](https://example.com/image.png)."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_combined_text(self):
        text = "Here is **bold**, _italic_, `code`, a [link](https://example.com), and an ![image](https://example.com/image.png)."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("Here is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(", a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(", and an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)
    

    def test_link_and_image_combined(self):
        text = "Check this [link](https://example.com) and ![image](https://example.com/image.png)."
        blocknode = BlockNode(text, 1)
        nodes = blocknode.block_text_to_text_nodes()
        expected = [
            TextNode("Check this ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.PLAIN)
            ]
        self.assertEqual(nodes, expected)

    def test_markdown_to_blocks(self):
        md = """This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                BlockNode("This is a **bolded** paragraph", 1),
                BlockNode("This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", 3),
                BlockNode("- This is a list\n- with items", 6),
            ],
        )

    def test_markdown_to_text_nodes(self):
        md = """This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        nodes = []
        for block in blocks:
            nodes.extend(block.block_text_to_text_nodes())
        self.assertEqual(
            nodes,
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" paragraph", TextType.PLAIN),
                TextNode("This is another paragraph with ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text and ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" here\nThis is the same paragraph on a new line", TextType.PLAIN),
            ]
        )