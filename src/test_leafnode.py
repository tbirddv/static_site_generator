import unittest
from htmlnode import LeafNode

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