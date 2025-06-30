import unittest
from split_nodes import *
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_plain_text(self):
        node = TextNode("This is a **bold** text", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_with_no_delimiter(self):
        node = TextNode("This is a plain text", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_split_with_odd_delimiters(self):
        node = TextNode("This is a **bold text with odd delimiter", TextType.PLAIN)
        with self.assertRaises(Exception) as context:
            split_node_at_delimiter([node], "**", TextType.BOLD)
        self.assertTrue("Did not find an even number of ** in" in str(context.exception))
    
    def test_split_multiple_delimiters(self):
        node = TextNode("This is a **bold** and _italic_ text", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_node_at_delimiter(new_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_matching_delimiters(self):
        node = TextNode("This is a **bold** text with **multiple** bold parts", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.PLAIN),
            TextNode("multiple", TextType.BOLD),
            TextNode(" bold parts", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** text at start", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text at start", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_end(self):
        node = TextNode("Text at end **Bold**", TextType.PLAIN)
        new_nodes = split_node_at_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Text at end ", TextType.PLAIN),
            TextNode("Bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_with_mixed_node_types(self):
        node1 = TextNode("This is a **bold** text", TextType.PLAIN)
        node2 = TextNode("This is already italic", TextType.ITALIC)
        node3 = TextNode("And this is a _italic_ text", TextType.PLAIN)
        node4 = TextNode("This is already bold", TextType.BOLD)
        node5 = TextNode("And this is a `code` text", TextType.PLAIN)
        node6 = TextNode("This is already code", TextType.CODE)
        node7 = TextNode("This is **mixed** text with _multiple_ delimiters", TextType.PLAIN)
        old_nodes = [node1, node2, node3, node4, node5, node6, node7]
        new_nodes = split_node_at_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = split_node_at_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_node_at_delimiter(new_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is already italic", TextType.ITALIC),
            TextNode("And this is a ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is already bold", TextType.BOLD),
            TextNode("And this is a ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is already code", TextType.CODE),
            TextNode("This is ", TextType.PLAIN),
            TextNode("mixed", TextType.BOLD),
            TextNode(" text with ", TextType.PLAIN),
            TextNode("multiple", TextType.ITALIC),
            TextNode(" delimiters", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_link_node(self):
        node = TextNode("This is text with a [link](https://example.com) inside", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" inside", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_image_node(self):
        node = TextNode("This is text with an ![image](https://example.com/image.png) inside", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" inside", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_only_link_node(self):
        node = TextNode("[link](https://example.com)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_only_image_node(self):
        node = TextNode("![image](https://example.com/image.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_mixed_nodes_with_links_and_images(self):
        node1 = TextNode("This is a [link](https://example.com) and an ![image](https://example.com/image.png)", TextType.PLAIN)
        node2 = TextNode("This is already bold", TextType.BOLD)
        old_nodes = [node1, node2]
        new_nodes = split_node_at_images(old_nodes)
        new_nodes = split_node_at_links(new_nodes)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("This is already bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_links_and_images(self):
        node = TextNode("This is a [link1](https://example1.com) and ![image1](https://example1.com/image1.png) and [link2](https://example2.com) and ![image2](https://example2.com/image2.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        new_nodes = split_node_at_links(new_nodes)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image1", TextType.IMAGE, "https://example1.com/image1.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image2", TextType.IMAGE, "https://example2.com/image2.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_empty_alt_text_image(self):
        node = TextNode("![](https://example.com/image.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_consecutive_links(self):
        node = TextNode("[link1](https://example1.com)[link2](https://example2.com)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode("link2", TextType.LINK, "https://example2.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_consecutive_images(self):
        node = TextNode("![image1](https://example1.com/image1.png)![image2](https://example2.com/image2.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("image1", TextType.IMAGE, "https://example1.com/image1.png"),
            TextNode("image2", TextType.IMAGE, "https://example2.com/image2.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_consecutive_links_and_images(self):
        node = TextNode("[link1](https://example1.com)![image1](https://example1.com/image1.png)[link2](https://example2.com)![image2](https://example2.com/image2.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        new_nodes = split_node_at_links(new_nodes)
        expected_nodes = [
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode("image1", TextType.IMAGE, "https://example1.com/image1.png"),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode("image2", TextType.IMAGE, "https://example2.com/image2.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_nested_brackets_in_link(self):
        node = TextNode("This is a [link with [nested brackets]](https://example.com)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link with [nested brackets]", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_nested_brackets_in_image(self):
        node = TextNode("This is an ![image with [nested brackets]](https://example.com/image.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("image with [nested brackets]", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_brackets_no_link(self):
        node = TextNode("This is a text with [brackets] but no link or ![image]", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        new_nodes = split_node_at_images(new_nodes)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_special_characters_in_link(self):
        node = TextNode("This is a [link with special characters !@#$%^&*()](https://example.com/#)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link with special characters !@#$%^&*()", TextType.LINK, "https://example.com/#")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_special_characters_in_image(self):
        node = TextNode("This is an ![image with special characters !@#$%^&*()](https://example.com/#$/image.png)", TextType.PLAIN)
        new_nodes = split_node_at_images([node])
        expected_nodes = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("image with special characters !@#$%^&*()", TextType.IMAGE, "https://example.com/#$/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_brackets_in_text_before_link(self):
        node = TextNode("Use array[0] and then [real link](https://example.com)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("Use array[0] and then ", TextType.PLAIN),
            TextNode("real link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_parentheses_in_text_before_link(self):
        node = TextNode("Call func() then [link](https://example.com)", TextType.PLAIN)
        new_nodes = split_node_at_links([node])
        expected_nodes = [
            TextNode("Call func() then ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    