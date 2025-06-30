import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode, ImageNode

class TestTextToLeafNode(unittest.TestCase):
    def test_plain_text(self):
        text_node = TextNode("Hello, World!", TextType.PLAIN)
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag=None, value="Hello, World!")
        self.assertEqual(leaf_node, expected_node)

    def test_bold_text(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag="b", value="Bold Text")
        self.assertEqual(leaf_node, expected_node)

    def test_italic_text(self):
        text_node = TextNode("Italic Text", TextType.ITALIC)
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag="i", value="Italic Text")
        self.assertEqual(leaf_node, expected_node)

    def test_code_text(self):
        text_node = TextNode("Code Snippet", TextType.CODE)
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag="code", value="Code Snippet")
        self.assertEqual(leaf_node, expected_node)

    def test_link_text(self):
        text_node = TextNode("OpenAI", TextType.LINK, "https://www.openai.com")
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag="a", value="OpenAI", props={"href": "https://www.openai.com"})
        self.assertEqual(leaf_node, expected_node)


    def test_link_without_text(self):
        text_node = TextNode("", TextType.LINK, "https://www.openai.com")
        with self.assertRaises(ValueError):
            text_node.to_html_node()

    def test_image_text(self):
        text_node = TextNode("Image Description", TextType.IMAGE, "https://example.com/image.png")
        leaf_node = text_node.to_html_node()
        expected_node = ImageNode(tag="img", props={"src": "https://example.com/image.png", "alt": "Image Description"})
        self.assertEqual(leaf_node, expected_node)
    
    def test_image_without_text(self):
        text_node = TextNode("", TextType.IMAGE, "https://example.com/image.png")
        leaf_node = text_node.to_html_node()
        expected_node = ImageNode(tag="img", props={"src": "https://example.com/image.png"})
        self.assertEqual(leaf_node, expected_node)

    def test_image_with_white_space_text(self):
        text_node = TextNode("   ", TextType.IMAGE, "https://example.com/image.png")
        leaf_node = text_node.to_html_node()
        expected_node = ImageNode(tag="img", props={"src": "https://example.com/image.png", "alt": "   "})
        self.assertEqual(leaf_node, expected_node)

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid Type", TextType.PLAIN)
        text_node.text_type = "INVALID"  # Simulating an invalid state
        with self.assertRaises(ValueError):
            text_node.to_html_node()

    def test_none_text_type(self):
        text_node = TextNode("None Type", TextType.PLAIN, None)
        text_node.text_type = None  # Simulating an invalid state
        with self.assertRaises(ValueError):
            text_node.to_html_node()

    def test_special_characters(self):
        text_node = TextNode("Special & Characters < > \" '", TextType.PLAIN)
        leaf_node = text_node.to_html_node()
        expected_node = LeafNode(tag=None, value="Special & Characters < > \" '")
        self.assertEqual(leaf_node, expected_node)

    def test_non_string_text(self):
        text_node = TextNode(12345, TextType.PLAIN)
        expected_node = LeafNode(tag=None, value=12345)
        leaf_node = text_node.to_html_node()
        html_output = expected_node.to_html()
        self.assertEqual(html_output, "12345")
        self.assertEqual(leaf_node, expected_node)
        
    def test_image_to_html(self):
        text_node = TextNode("Image Description", TextType.IMAGE, "https://example.com/image.png")
        leaf_node = text_node.to_html_node()
        self.assertIsInstance(leaf_node, ImageNode)
        html_output = leaf_node.to_html()
        expected_html = '<img src="https://example.com/image.png" alt="Image Description" />'
        self.assertEqual(html_output, expected_html)


        
