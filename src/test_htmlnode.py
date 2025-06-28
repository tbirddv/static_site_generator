import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_with_tag_and_value(self):
        node = HTMLNode(tag="div", value="Hello World")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_init_with_children(self):
        child_node = HTMLNode(tag="span", value="Child Node")
        node = HTMLNode(tag="div", children=[child_node])
        self.assertEqual(node.children, [child_node])

    def test_init_with_props(self):
        node = HTMLNode(tag="div", value="div", props={"class": "container"})
        self.assertEqual(node.props, {"class": "container"})

    def test_with_all_params(self):
        child_node = HTMLNode(tag="span", value="Child Node")
        node = HTMLNode(tag="div", value="Parent Node", children=[child_node], props={"class": "container"})
        node2 = HTMLNode(tag="div", value="Parent Node", children=[child_node], props={"class": "container"})
        self.assertEqual(node, node2)
    
    def test_eq(self):
        node = HTMLNode(tag="div", value="Hello World")
        node2 = HTMLNode(tag="div", value="Hello World")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode(tag="div", value="Hello World")
        node2 = HTMLNode(tag="div", value="Goodbye World")
        self.assertNotEqual(node, node2)

    def test_eq_all_params(self):
        child_node = HTMLNode(tag="span", value="Child Node")
        node = HTMLNode(tag="div", value="Parent Node", children=[child_node], props={"class": "container"})
        node2 = HTMLNode(tag="div", value="Parent Node", children=[child_node], props={"class": "container"})
        self.assertEqual(node, node2)

    def test_not_eq_different_tags(self):
        node = HTMLNode(tag="div", value="Hello World")
        node2 = HTMLNode(tag="span", value="Hello World")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_props(self):
        node = HTMLNode(tag="div", value="Hello World", props={"class": "container"})
        node2 = HTMLNode(tag="div", value="Hello World", props={"class": "different"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello World", props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=Hello World, props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_children(self):
        child_node = HTMLNode(tag="span", value="Child Node")
        node = HTMLNode(tag="div", value="Parent Node", children=[child_node], props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=Parent Node, children=[HTMLNode(tag=span, value=Child Node)], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    


    def test_init_without_value_or_children(self):
        with self.assertRaises(ValueError):
            HTMLNode(tag="div")

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="Hello World")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html(self):
        node = HTMLNode(tag="div", value="div", props={"class": "container", "id": "main"})
        node2 = HTMLNode(tag="<a>", value="link", props={"href": "https://example.com"})
        node3 = HTMLNode(tag="<a>", value="test image", props={"src": "https://example.com/image.png"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
        self.assertEqual(node2.props_to_html(), ' href="https://example.com"')
        self.assertEqual(node3.props_to_html(), ' src="https://example.com/image.png"')
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)