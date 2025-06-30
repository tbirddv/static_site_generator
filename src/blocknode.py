import re
from enum import Enum
from htmlnode import LeafNode, ImageNode, ParentNode
from textnode import TextNode, TextType
from split_nodes import split_node_at_delimiter, split_node_at_links, split_node_at_images

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

class BlockNode:
    def __init__(self, content, start_line):
        self.content = content
        self.start_line = start_line
        self.block_type = self.determine_block_type()

    def determine_block_type(self):
        if re.match(r"#{1,6} ", self.content) and len(self.content.split("\n")) == 1:
            return BlockType.HEADING
        elif re.match(r"^```$.*^```$", self.content, re.DOTALL | re.MULTILINE):
            return BlockType.CODE
        else:
            could_be_quote = True
            could_be_unordered_list = True
            could_be_ordered_list = True
            newline = 0
            for line in self.content.split("\n"):
                newline += 1
                if not re.match(r"> ", line):
                    could_be_quote = False
                if not re.match(r"- ", line):
                    could_be_unordered_list = False
                if not line.startswith(str(newline) + ". "):
                    could_be_ordered_list = False
            if could_be_quote:
                return BlockType.QUOTE
            elif could_be_unordered_list:
                return BlockType.UNORDERED_LIST
            elif could_be_ordered_list:
                return BlockType.ORDERED_LIST
            else:
                return BlockType.PARAGRAPH
            
    def __eq__(self, other):
        if not isinstance(other, BlockNode):
            return False
        return (self.content == other.content and
                self.start_line == other.start_line and
                self.block_type == other.block_type)
    
    def __repr__(self):
        return f"BlockNode(content={self.content}, start_line={self.start_line}, block_type={self.block_type.value})"
            
    def block_text_to_text_nodes(self, text=None):
        if text is None:
            text = self.content
        nodes = [TextNode(text, TextType.PLAIN)]
        start_line = self.start_line
        end_line = start_line + self.content.count('\n')
        if "**" in self.content:
            try:
                nodes = split_node_at_delimiter(nodes, "**", TextType.BOLD)
            except ValueError as e:
                print(f"Error processing bold text in lines {start_line}-{end_line}: {e}")
                if input("Continue? (y/n): ").lower() != 'y':
                    raise ValueError(f"Error processing bold text: {e}")
                else:
                    print("Continuing without bold text processing.")
        if "_" in self.content:
            try:
                nodes = split_node_at_delimiter(nodes, "_", TextType.ITALIC)
            except ValueError as e:
                print(f"Error processing italic text in lines {start_line}-{end_line}: {e}")
                if input("Continue? (y/n): ").lower() != 'y':
                    raise ValueError(f"Error processing italic text: {e}")
                else:
                    print("Continuing without italic text processing.")
        if "`" in self.content:
            try:
                nodes = split_node_at_delimiter(nodes, "`", TextType.CODE)
            except ValueError as e:
                print(f"Error processing code text in lines {start_line}-{end_line}: {e}")
                if input("Continue? (y/n): ").lower() != 'y':
                    raise ValueError(f"Error processing inline code text: {e}")
                else:
                    print("Continuing without inline code text processing.")
        if "](" in self.content:
            print(f"Processing images and links in lines: {start_line}-{end_line}, please confirm syntax if output is unexpected.")
            print("See README.md for more information on supported markdown syntax.")
            nodes = split_node_at_images(nodes)
            nodes = split_node_at_links(nodes)
        return nodes

    def to_parent_node(self):
        if self.block_type == BlockType.PARAGRAPH:
            current_line = self.start_line - 1
            for line in self.content.split("\n"):
                current_line += 1
                if line.startswith("#"):
                    print(f"Warning:\nblock:\n {self.content} \nstarting at line: {self.start_line} was detected as a paragraph but appears to contain a heading at line {current_line}. This may be a syntax error.")
                    print(f" If this is a heading please add a blank line before and after it to separate it from the surrounding blocks. Otherwise type 'y' to continue processing as a paragraph.")
                    print("Reminder: Headings should consist of a single line starting with one or more '#' characters followed by a space.")
                    if input("Continue? (y/n): ").lower() != 'y':
                        raise ValueError(f"Syntax Error Confirmed in block starting at line {self.start_line}. Please confirm supported markdown syntax in README.md.")
                    else:
                        print("Continuing processing as a paragraph. No other syntax errors will be checked in this block.")
                        break
                if "```" in line:
                    print(f"Warning:\nblock:\n {self.content} \nstarting at line: {self.start_line} was detected as a paragraph but appears to contain a code block starting at line: {current_line}. This may be a syntax error.")
                    print(f" If this is a code block please review README.md for supported syntax. Otherwise type 'y' to continue processing as a paragraph.")
                    print(f"Reminder: Inline code is supported in paragraphs with a single backtick (`) on either side of the code. Block code is supported with three backticks (```), but must be separated on either side by a blank line.")
                    if input("Continue? (y/n): ").lower() != 'y':
                        raise ValueError(f"Syntax Error Confirmed in block starting at line {self.start_line}. Please confirm supported markdown syntax in README.md.")
                    else:
                        print("Continuing processing as a paragraph. No other syntax errors will be checked in this block.")
                        break
                if line.startswith("> "):
                    print(f"Warning:\nblock:\n {self.content} \nstarting at line: {self.start_line} was detected as a paragraph but appears to contain a quote starting at line: {current_line}. This may be a syntax error.")
                    print(f" If this is a quote please review README.md for supported syntax. Otherwise type 'y' to continue processing as a paragraph.")
                    print("Reminder: Block quotes should start with '> ' at the beginning of each line and should be separated on either side by a blank line.")
                    if input("Continue? (y/n): ").lower() != 'y':
                        raise ValueError(f"Syntax Error Confirmed in block starting at line {self.start_line}. Please confirm supported markdown syntax in README.md.")
                    else:
                        print("Continuing processing as a paragraph. No other syntax errors will be checked in this block.")
                        break
                if line.startswith("- ") or re.match(r"^\d+\. ", line):
                    print(f"Warning:\nblock:\n {self.content} \nstarting at line: {self.start_line} was detected as a paragraph but appears to contain a list starting at line: {current_line}. This may be a syntax error.")
                    print(f" If this is a list please review README.md to confirm supported syntax. Otherwise type 'y' to continue processing as a paragraph.")
                    print("Reminder: Unordered lists should start with '- ' at the beginning of each line and ordered lists should start with '1. ', '2. ', etc. at the beginning of each line, and should be separated on either side by a blank line.")
                    if input("Continue? (y/n): ").lower() != 'y':
                        raise ValueError(f"Syntax Error Confirmed in block starting at line {self.start_line}. Please confirm supported markdown syntax in README.md.")
                    else:
                        print("Continuing processing as a paragraph. No other syntax errors will be checked in this block.")
                        break
            return ParentNode(tag="p", children=[node.to_html_node() for node in self.block_text_to_text_nodes()])
        elif self.block_type == BlockType.HEADING:
            level = re.match(r"#{1,6}", self.content).group(0)
            self.content = self.content.lstrip("#")
            return ParentNode(tag=f"h{len(level)}", children=[node.to_html_node() for node in self.block_text_to_text_nodes()])
        elif self.block_type == BlockType.CODE:
            self.content = self.content.lstrip("```\n")
            self.content = self.content.rstrip("\n```")
            return ParentNode(tag="pre", children=[LeafNode(tag="code", value=self.content)])
        elif self.block_type == BlockType.QUOTE:
            self.content = "\n".join(line.lstrip("> ") for line in self.content.split("\n"))
            return ParentNode(tag="blockquote", children=[node.to_html_node() for node in self.block_text_to_text_nodes()])
        elif self.block_type == BlockType.UNORDERED_LIST:
            self.content = "\n".join(line.lstrip("- ") for line in self.content.split("\n"))
            return ParentNode(tag="ul", children=[ParentNode(tag="li", children=[node.to_html_node() for node in self.block_text_to_text_nodes(line)]) for line in self.content.split("\n")])
        elif self.block_type == BlockType.ORDERED_LIST:
            self.content = "\n".join(line.lstrip(f"{i+1}. ") for i, line in enumerate(self.content.split("\n")))
            return ParentNode(tag="ol", children=[ParentNode(tag="li", children=[node.to_html_node() for node in self.block_text_to_text_nodes(line)]) for line in self.content.split("\n")])
        else:
            raise ValueError(f"Unsupported BlockType: {self.block_type}")
        
        def to_section(self):
            return ParentNode(tag=div, children=[self.to_parent_node()])