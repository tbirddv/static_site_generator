import unittest
from htmlnode import LeafNode, ImageNode

class TestLeafNode(unittest.TestCase):
    def test_init_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_init_with_props(self):
        node = LeafNode(tag="img", value="google.com", props={"href": "google.com"})
        node2 = LeafNode(tag="img", value="google.com", props={"href": "google.com"})
        self.assertEqual(node, node2)

    def test_init_with_multiple_props(self):
        node = LeafNode("a", "Visit Google", {"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("a", "Visit Google", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_init_with_no_tag(self):
        node = LeafNode(tag=None, value="Just a text node")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Just a text node")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_to_html(self):
        node = LeafNode(tag="p", value="Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_to_html_multiple_props(self):
        node = LeafNode("a", "Visit Google", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Visit Google</a>')

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Just a text node")
        self.assertEqual(node.to_html(), "Just a text node")

    def test_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click Me!", props={"href": "example.com"})
        self.assertEqual(node.to_html(), '<a href="example.com">Click Me!</a>')

    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value="")

class TestImageNode(unittest.TestCase):
    def test_init(self):
        node = ImageNode("img", {"src": "https://example.com/image.png", "alt": "Example Image"})
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.props, {"src": "https://example.com/image.png", "alt": "Example Image"})
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])

    def test_to_html(self):
        node = ImageNode("img", {"src": "https://example.com/image.png", "alt": "Example Image"})
        self.assertEqual(node.to_html(), '<img src="https://example.com/image.png" alt="Example Image" />')

    def test_to_html_with_no_alt(self):
        node = ImageNode("img", {"src": "https://example.com/image.png"})
        self.assertEqual(node.to_html(), '<img src="https://example.com/image.png" />')

    def test_no_src(self):
        with self.assertRaises(ValueError):
            ImageNode("img", {"alt": "Example Image"})

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ImageNode("", {"src": "https://example.com/image.png", "alt": "Example Image"})

    def test_no_props(self):
        with self.assertRaises(ValueError):
            ImageNode("img", {})

    def test_src_not_string(self):
        with self.assertRaises(TypeError):
            ImageNode("img", {"src": 123, "alt": "Example Image"})