import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode, ImageNode
from split_nodes import split_node_at_delimiter, split_node_at_links, split_node_at_images
from blocknode import BlockType, BlockNode

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    blocks = []
    start_line = 1
    i = 0
    while i < len(lines):
        # gather lines until you hit a blank
        if lines[i].strip() == "":
            i += 1
            start_line += 1
            continue
        block_lines = []
        block_start = start_line
        while i < len(lines) and lines[i].strip() != "":
            block_lines.append(lines[i])
            i += 1
            start_line += 1
        blocks.append(BlockNode("\n".join(block_lines).strip(), block_start))
    return blocks    

def main():
    # Example usage
    markdown = "This is **bold** text.\n\nThis is _italic_ text.\n\nThis is `code` text.\n\nThis is a [link](https://example.com).\n\nThis is an ![image](https://example.com/image.png)."
    blocks = markdown_to_blocks(markdown)
    
        
    

if __name__ == "__main__":
    main()