import re
from htmlnode import *
from textnode import TextNode, TextType

def check_delimter_syntax(node, delimiter):
    count = node.text.count(delimiter)
    if count % 2 == 0:
        return True
    return False

def split_node_at_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type.PLAIN:
            new_nodes.append(node)
            continue
        if not check_delimter_syntax(node, delimiter):
            raise Exception(f"Did not find an even number of {delimiter} in {node.text}. Markdown syntax requires opening and closing delimiters to be in pairs.")
        parts = node.text.split(delimiter)
        plain_nodes = [TextNode(part, node.text_type) for part in parts[::2]]
        text_type_nodes = [TextNode(part, text_type) for part in parts[1::2]]
        for i in range(max(len(plain_nodes), len(text_type_nodes))):
            if i < len(plain_nodes) and plain_nodes[i].text:
                new_nodes.append(plain_nodes[i])
            if i < len(text_type_nodes) and text_type_nodes[i].text:
                new_nodes.append(text_type_nodes[i])
    return new_nodes

def search_for_link(old_node):
    return re.search(r'\[([^\]]+)[\]\(]([^)]+)\)', old_node.text)
    

def split_node_at_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        # Find all valid markdown links first
        link_pattern = r'\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]\(([^)]+)\)'
        links = list(re.finditer(link_pattern, node.text))
        
        if not links:
            new_nodes.append(node)
            continue
            
        # Split based on the actual found links
        last_end = 0
        for match in links:
            # Add text before the link
            if match.start() > last_end:
                before_text = node.text[last_end:match.start()]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.PLAIN))
            
            # Add the link
            text, url = match.groups()
            new_nodes.append(TextNode(text, TextType.LINK, url))
            last_end = match.end()
        
        # Add any remaining text
        if last_end < len(node.text):
            remaining_text = node.text[last_end:]
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_nodes
    
def search_for_image(old_node):
    return re.search(r'!\[(.*)[\]\(]([^)]+)\)', old_node.text)

def split_node_at_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if not search_for_image(node):
            new_nodes.append(node)
            continue
        parts = re.split(r'(!\[.*?[\]\(].+?\))', node.text)
        for part in parts:
            if not part.strip():
                continue
            if part.startswith("![") and part.endswith(")"):
                match = re.match(r'!\[(.*?)\]\((.+)\)', part)
                if match:
                    alt_text, url = match.groups()
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(part, TextType.PLAIN))
    return new_nodes
