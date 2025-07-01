import unittest
from blocknode import BlockNode, BlockType
from htmlnode import ParentNode, LeafNode, ImageNode

class TestBlockToSection(unittest.TestCase):
    def test_block_to_section(self):
        block = BlockNode("This is a paragraph.", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="p", children=[LeafNode(tag=None, value="This is a paragraph.", props=None)])])
        self.assertEqual(section, expected_section)

    def test_heading_block_to_section(self):
        block = BlockNode("# This is a heading", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="h1", children=[LeafNode(tag=None, value="This is a heading", props=None)])])
        self.assertEqual(section, expected_section)

    def test_code_block_to_section(self):
        block = BlockNode("```\nprint('Hello, World!')\n```", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="pre", children=[LeafNode(tag="code", value="print('Hello, World!')", props=None)])])
        self.assertEqual(section, expected_section)

    def test_quote_block_to_section(self):
        block = BlockNode("> This is a quote", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="blockquote", children=[LeafNode(tag=None, value="This is a quote", props=None)])])
        self.assertEqual(section, expected_section)

    def test_unordered_list_block_to_section(self):
        block = BlockNode("- Item 1\n- Item 2", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[
            ParentNode(tag="ul", children=[
                ParentNode(tag="li", children=[LeafNode(tag=None, value="Item 1", props=None)]),
                ParentNode(tag="li", children=[LeafNode(tag=None, value="Item 2", props=None)])
            ])
        ])
        self.assertEqual(section, expected_section)

    def test_ordered_list_block_to_section(self):
        block = BlockNode("1. First item\n2. Second item", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[
            ParentNode(tag="ol", children=[
                ParentNode(tag="li", children=[LeafNode(tag=None, value="First item", props=None)]),
                ParentNode(tag="li", children=[LeafNode(tag=None, value="Second item", props=None)])
            ])
        ])
        self.assertEqual(section, expected_section)

    def test_multi_line_quote_block_to_section(self):
        block = BlockNode("> This is a quote\n> that spans multiple lines", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="blockquote", children=[
            LeafNode(tag=None, value="This is a quote\nthat spans multiple lines", props=None)
        ])])
        self.assertEqual(section, expected_section)

    def test_paragraph_with_newline_to_section(self):
        block = BlockNode("This is a paragraph.\nWith a newline.", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="p", children=[
            LeafNode(tag=None, value="This is a paragraph.\nWith a newline.", props=None)
        ])])
        self.assertEqual(section, expected_section)

    def test_paragraph_with_inline_delimiter(self):
        block = BlockNode("This is a paragraph with **bold** text.", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[ParentNode(tag="p", children=[
            LeafNode(tag=None, value="This is a paragraph with ", props=None),
            LeafNode(tag="b", value="bold", props=None),
            LeafNode(tag=None, value=" text.", props=None)
        ])])
        self.assertEqual(section, expected_section)

    def test_paragraph_with_image(self):
        block = BlockNode("This is an ![image](https://example.com/image.png).", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[
            ParentNode(tag="p", children=[
                LeafNode(tag=None, value="This is an ", props=None),
                ImageNode(tag="img", props={"src": "https://example.com/image.png", "alt": "image"}),
                LeafNode(tag=None, value=".", props=None)
            ])
        ])
        self.assertEqual(section, expected_section)

    def test_block_to_html(self):
        block = BlockNode("This is a paragraph.", 1)
        section = block.to_section()
        html = section.to_html()
        expected_html = '<div><p>This is a paragraph.</p></div>'
        self.assertEqual(html, expected_html)

    def test_code_block_with_inline_delimiters(self):
        block = BlockNode("```\nprint('Hello, **World!**')\n```", 1)
        section = block.to_section()
        expected_section = ParentNode(tag="div", children=[
            ParentNode(tag="pre", children=[
                LeafNode(tag="code", value="print('Hello, **World!**')", props=None)
            ])
        ])
        self.assertEqual(section, expected_section)