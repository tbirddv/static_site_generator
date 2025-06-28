import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_init_with_tag_and_children(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child_node])
        self.assertEqual(node.props, {})

    def test_init_with_props(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node], props={"class": "container"})
        self.assertEqual(node.props, {"class": "container"})

    def test_non_ascii_value(self):
        child_node = LeafNode(tag="span", value="子节点")
        node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(node.to_html(), "<div><span>子节点</span></div>")
    
    def test_special_characters_in_props(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node], props={"data-info": "value with spaces and & characters"})
        self.assertEqual(node.to_html(), '<div data-info="value with spaces and & characters"><span>Child Node</span></div>')

    def test_duplicate_tag_and_props(self):
        child_node_1 = LeafNode(tag="span", value="Child Node 1", props={"class": "highlight"})
        child_node_2 = LeafNode(tag="span", value="Child Node 2", props={"class": "highlight"})
        node = ParentNode(tag="div", children=[child_node_1, child_node_2], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span class="highlight">Child Node 1</span><span class="highlight">Child Node 2</span></div>')

    def test_to_html(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(node.to_html(), "<div><span>Child Node</span></div>")

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode(tag="span", value="Child Node 1")
        child_node2 = LeafNode(tag="span", value="Child Node 2")
        node = ParentNode(tag="div", children=[child_node1, child_node2])
        self.assertEqual(node.to_html(), "<div><span>Child Node 1</span><span>Child Node 2</span></div>")

    def test_to_html_with_multiple_children_and_props(self):
        child_node1 = LeafNode(tag="span", value="Child Node 1")
        child_node2 = LeafNode(tag="span", value="Child Node 2")
        node = ParentNode(tag="div", children=[child_node1, child_node2], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>Child Node 1</span><span>Child Node 2</span></div>')

    def test_to_html_multiple_children_where_one_has_props(self):
        child_node1 = LeafNode(tag="span", value="Child Node 1")
        child_node2 = LeafNode(tag="span", value="Child Node 2", props={"class": "highlight"})
        node = ParentNode(tag="div", children=[child_node1, child_node2])
        self.assertEqual(node.to_html(), '<div><span>Child Node 1</span><span class="highlight">Child Node 2</span></div>')

    def test_repr(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node], props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, children=[HTMLNode(tag=span, value=Child Node)], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_with_props(self):
        child_node = LeafNode(tag="span", value="Child Node")
        node = ParentNode(tag="div", children=[child_node], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>Child Node</span></div>')

    def test_grandchildren(self):
        grandchild_node = LeafNode(tag="p", value="Grandchild Node")
        child_node = ParentNode(tag="div", children=[grandchild_node])
        node = ParentNode(tag="section", children=[child_node])
        self.assertEqual(node.to_html(), "<section><div><p>Grandchild Node</p></div></section>")

    def test_great_grandchildren(self):
        great_grandchild_node = LeafNode(tag="span", value="Great Grandchild Node")
        grandchild_node = ParentNode(tag="p", children=[great_grandchild_node])
        child_node = ParentNode(tag="div", children=[grandchild_node])
        node = ParentNode(tag="section", children=[child_node])
        self.assertEqual(node.to_html(), "<section><div><p><span>Great Grandchild Node</span></p></div></section>")

    def test_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=[])

    def test_non_htmlnode_choildren(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="div", children=["Not an HTMLNode"])

    def test_deep_recursion(self):
        level_ten = LeafNode(tag="span", value="Level 10")
        level_nine = ParentNode(tag="div", children=[level_ten])
        level_eight = ParentNode(tag="div", children=[level_nine])
        level_seven = ParentNode(tag="div", children=[level_eight])
        level_six = ParentNode(tag="div", children=[level_seven])
        level_five = ParentNode(tag="div", children=[level_six])
        level_four = ParentNode(tag="div", children=[level_five])
        level_three = ParentNode(tag="div", children=[level_four])
        level_two = ParentNode(tag="div", children=[level_three])
        root_node = ParentNode(tag="div", children=[level_two])
        self.assertEqual(root_node.to_html(), "<div><div><div><div><div><div><div><div><div><span>Level 10</span></div></div></div></div></div></div></div></div></div>")

    def test_mixed_children(self):
        child_node1 = LeafNode(tag="span", value="Child Node 1")
        child_node2 = ParentNode(tag="div", children=[LeafNode(tag="p", value="Child Node 2")])
        node = ParentNode(tag="section", children=[child_node1, child_node2])
        self.assertEqual(node.to_html(), "<section><span>Child Node 1</span><div><p>Child Node 2</p></div></section>")

    def test_mixed_props_and_no_props(self):
        child_node1 = LeafNode(tag="span", value="Child Node 1", props={"class": "highlight"})
        child_node2 = ParentNode(tag="div", children=[LeafNode(tag="p", value="Child Node 2")], props={"class": "highlight"})
        child_node3 = LeafNode(tag="span", value="Child Node 3")
        node = ParentNode(tag="section", children=[child_node1, child_node2, child_node3])
        self.assertEqual(node.to_html(), '<section><span class="highlight">Child Node 1</span><div class="highlight"><p>Child Node 2</p></div><span>Child Node 3</span></section>')

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[LeafNode(tag="span", value="Child Node")])