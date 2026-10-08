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
    opening, code_text = block.split("\n", 1)
    code_text = code_text[:-3]
    language = opening[3:]
    props = {"class": "language-" + language} if language else None
    code_node = LeafNode("code", code_text, props)
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


def parse_frontmatter(markdown):
    if not markdown.startswith("---\n"):
        return {}, markdown
    metadata, separator, content = markdown[4:].partition("\n---\n")
    if not separator:
        raise ValueError("Frontmatter must end with ---")
    values = {}
    for line in metadata.splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator or key.strip() not in {"description", "layout"}:
            raise ValueError(f"Unsupported frontmatter: {line}")
        values[key.strip()] = value.strip()
    if values.get("layout", "page") not in {"home", "page"}:
        raise ValueError("Layout must be home or page")
    return values, content


def normalize_basepath(basepath):
    if not basepath.startswith("/") or any(
        part in {".", ".."} for part in basepath.split("/")
    ):
        raise ValueError("Base path must be an absolute URL path without traversal")
    if any(char in basepath for char in '"<>?#\\'):
        raise ValueError("Base path contains unsupported characters")
    return "/" + basepath.strip("/") + "/" if basepath.strip("/") else "/"


def generate_page(
    from_path,
    template_path,
    dest_path,
    basepath="/",
    *,
    route="/",
    site_url="https://yaqyn.github.io/folio",
):
    from html import escape
    from pathlib import Path
    import re

    basepath = normalize_basepath(basepath)
    print(f"Generating {route}")
    metadata, markdown = parse_frontmatter(Path(from_path).read_text(encoding="utf-8"))
    template = Path(template_path).read_text(encoding="utf-8")
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    description = metadata.get(
        "description", f"{title} — projects and notes by Abdulrahman M. Yaqyn."
    )
    layout = metadata.get("layout", "page")
    navigation = []
    for label, target in [
        ("Home", "/"),
        ("Projects", "/projects/"),
        ("Notes", "/notes/"),
        ("About", "/about/"),
    ]:
        selected = route == target if target == "/" else route.startswith(target)
        current = (
            f' aria-current="{"page" if route == target else "location"}"'
            if selected
            else ""
        )
        navigation.append(f'<a href="{target}"{current}>{label}</a>')
    replacements = {
        "Title": escape(title),
        "Content": html,
        "Description": escape(description, quote=True),
        "PageClass": layout,
        "Navigation": "".join(navigation),
        "Canonical": escape(site_url.rstrip("/") + route, quote=True),
        "ImageURL": escape(
            site_url.rstrip("/") + "/images/yaqyn-cover.png", quote=True
        ),
        "Breadcrumbs": '<a href="/">yaqyn.</a><span aria-hidden="true"> / </span>'
        + escape(title)
        if layout != "home"
        else "",
    }
    template = re.sub(
        r"\{\{ (\w+) \}\}",
        lambda match: replacements.get(match.group(1), match.group(0)),
        template,
    )
    # Prefix root-local href/src attributes, preserving protocol-relative URLs.
    template = re.sub(
        r'(href|src)="/(?!/)', lambda match: match.group(1) + '="' + basepath, template
    )
    destination = Path(dest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template, encoding="utf-8")
