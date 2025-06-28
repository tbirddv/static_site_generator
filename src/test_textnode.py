import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_long_text_eq(self):
        long_text = "This is a very long text node that should be equal to another long text node with the same content."
        node = TextNode(long_text, TextType.PLAIN)
        node2 = TextNode(long_text, TextType.PLAIN)
        self.assertEqual(node, node2)

    def test_not_string_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_not_None_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(This is a text node, BOLD)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        expected_repr = "TextNode(This is a link, LINK, https://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        expected_repr = "TextNode(This is an image, IMAGE, https://example.com/image.png)"
        self.assertEqual(repr(node), expected_repr)

    def test_text_type_enum(self):
        self.assertEqual(TextType.PLAIN.value, "PLAIN")
        self.assertEqual(TextType.BOLD.value, "BOLD")
        self.assertEqual(TextType.ITALIC.value, "ITALIC")
        self.assertEqual(TextType.CODE.value, "CODE")
        self.assertEqual(TextType.LINK.value, "LINK")
        self.assertEqual(TextType.IMAGE.value, "IMAGE")

    def test_not_eq_different_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, "This is a text node")

    def test_invalid_url_for_non_link_image(self):
        with self.assertRaises(ValueError):
            TextNode("This is a text node", TextType.PLAIN, "https://example.com")
    
    def test_missing_url_for_link(self):
        with self.assertRaises(ValueError):
            TextNode("This is a link", TextType.LINK)

    def test_missing_url_for_image(self):
        with self.assertRaises(ValueError):
            TextNode("This is an image", TextType.IMAGE)
    
    def test_working_url_for_link_image(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.text, "This is a link")

    def test_eq_url(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_eq_image(self):
        node1 = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        node2 = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(node1, node2)
    
    def test_not_eq_url(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_blank_text(self):
        node = TextNode("", TextType.PLAIN)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.PLAIN)
        self.assertIsNone(node.url)

    def test_blank_text_with_url(self):
        node = TextNode("", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    


if __name__ == "__main__":
    unittest.main()