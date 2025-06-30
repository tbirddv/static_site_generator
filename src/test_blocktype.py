import unittest
from blocknode import BlockType, BlockNode

class TestBlockType(unittest.TestCase):
    def test_paragraph_block(self):
        block = BlockNode("This is a paragraph.", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_block(self):
        block = BlockNode("# This is a heading", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):
        block = BlockNode("```\nprint('Hello, World!')\n```", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block(self):
        block = BlockNode("> This is a quote", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = BlockNode("- Item 1\n- Item 2", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = BlockNode("1. First item\n2. Second item", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_multi_line_quote_block(self):
        block = BlockNode("> This is a quote\n> that spans multiple lines", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_paragrphaph_with_newline(self):
        block = BlockNode("This is a paragraph.\nWith a newline.", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_paragraph_starting_with_number(self):
        block = BlockNode("1. This is a paragraph starting with a number.\nThis is still part of the same paragraph.", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_pharagraph_with_special_characters(self):
        block = BlockNode("This is a paragraph with special characters: @, #, $, %, &, *.", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def paragraph_starting_with_dash(self):
        block = BlockNode("- This is a paragraph starting with a dash.\nThis is still part of the same paragraph.", 1)
        block_type = block.block_type
        self.assertEqual(block_type, BlockType.PARAGRAPH)