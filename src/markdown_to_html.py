from block_markdown import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node
import os


def _text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def _text_block_to_parent(tag: str, text: str) -> ParentNode:
    return ParentNode(tag, _text_to_children(text))


def _heading_to_html(block: str) -> ParentNode:
    heading_text = block.lstrip("#")
    level = len(block) - len(heading_text)
    return _text_block_to_parent(f"h{level}", heading_text[1:])


def _list_to_html(block: str, tag: str, ordered: bool = False) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if ordered:
            item_text = line.split(". ", 1)[1]
        else:
            item_text = line[2:]
        items.append(ParentNode("li", _text_to_children(item_text)))
    return ParentNode(tag, items)


def _quote_to_html(block: str) -> ParentNode:
    quote_text = " ".join(line[1:].lstrip() for line in block.split("\n"))
    return _text_block_to_parent("blockquote", quote_text)


def _code_to_html(block: str) -> ParentNode:
    code_text = block[4:-3]
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def markdown_to_html_node(markdown: str) -> ParentNode:
    block_nodes = []

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            block_nodes.append(_heading_to_html(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(_code_to_html(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(_quote_to_html(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(_list_to_html(block, "ul"))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(_list_to_html(block, "ol", ordered=True))
        else:
            paragraph_text = " ".join(block.split("\n"))
            block_nodes.append(_text_block_to_parent("p", paragraph_text))

    return ParentNode("div", block_nodes)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Markdown document has no h1 heading")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath="/"):
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as output_file:
        output_file.write(page)
