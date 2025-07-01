import os
import shutil
import sys
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

def clone_directory_and_generate(src, dst, template):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(dst):
        item_path = os.path.join(dst, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        if os.path.isfile(src_item):
            shutil.copy2(src_item, dst_item)
            if item.endswith(".md"):
                dst_html = os.path.join(dst, item[:-3] + ".html")
                generate_page(dst_item, template, dst_html)
        elif os.path.isdir(src_item):
            clone_directory_and_generate(src_item, dst_item, template)

def get_title(blocks):
    for block in blocks:
        if block.block_type == BlockType.HEADING:
            if block.content.startswith("# "):
                return block.content[2:].strip()
    raise ValueError("Converter requires a title for website. Please add a level 1 heading.")

def generate_page(src, template, dst):
    print(f"Generating page from {src} using template {template} to {dst}")
    abs_src = os.path.abspath(src)
    abs_template = os.path.abspath(template)
    abs_dst = os.path.abspath(dst)
    if not os.path.exists(abs_src):
        raise FileNotFoundError(f"Source file '{abs_src}' does not exist.")
    if not os.path.exists(abs_template):
        raise FileNotFoundError(f"Template file '{abs_template}' does not exist.")
    if not os.path.exists(os.path.dirname(abs_dst)):
            os.makedirs(os.path.dirname(abs_dst))
    with open(abs_src, 'r', encoding='utf-8') as f:
        markdown = f.read()
    with open(abs_template, 'r', encoding='utf-8') as f:
        template_html = f.read()

    blocks = markdown_to_blocks(markdown)
    title = get_title(blocks)
    body_html = "\n".join(block.to_section().to_html() for block in blocks)
    if len(sys.argv) >= 2:
        output_html = template_html.replace("{{ Title }}", title).replace("{{ Content }}", body_html).replace('href="/', f'href="{sys.argv[1]}').replace('src="/', f'src="{sys.argv[1]}')
    with open(abs_dst, 'w', encoding='utf-8') as f:
        f.write(output_html)


def main():
    if len(sys.argv) == 4:
        src = sys.argv[1]
        dst = sys.argv[2]
        template = sys.argv[3]
        clone_directory_and_generate(src, dst, template)
        return
    if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("For Testing or Local Hosting:")
        print("Usage: python3 src/main.py <source_directory> <destination_directory> <template_file>")
        print("Example: python3 src/main.py static public template.html")
        print("For Production Build:")
        print("if hosting on GitHub Pages, provide the repository name as the second argument to ensure correct asset linking.")
        print("Usage: python3 src/main.py '/REPO_NAME/'")
        return
    if len(sys.argv) == 2:
        src = "static"
        template = "template.html"
        dst = "docs"
        clone_directory_and_generate(src, dst, template)

    
        
    

if __name__ == "__main__":
    main()