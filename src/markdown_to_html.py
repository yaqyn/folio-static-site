from block_markdown import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node
import os
import re
import struct
import unicodedata
from xml.etree import ElementTree


def _text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def _text_block_to_parent(tag: str, text: str) -> ParentNode:
    return ParentNode(tag, _text_to_children(text))


def _heading_to_html(block: str) -> ParentNode:
    lines = block.splitlines()
    if len(lines) == 2 and re.fullmatch(r" {0,3}(=+|-+)[ \t]*", lines[1]):
        return _text_block_to_parent("h1" if "=" in lines[1] else "h2", lines[0].strip())
    heading_text = block.lstrip("#")
    level = len(block) - len(heading_text)
    # CommonMark permits an optional closing run of hashes when it is
    # separated from the heading text by whitespace.
    text = heading_text[1:]
    text = re.sub(r"[ \t]+#+[ \t]*$", "", text)
    return _text_block_to_parent(f"h{level}", text)


def _list_to_html(block: str, tag: str, ordered: bool = False) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if ordered:
            item_text = re.split(r"[.)] ", line, maxsplit=1)[1]
        else:
            item_text = line[2:]
        items.append(ParentNode("li", _text_to_children(item_text)))
    props = None
    if ordered:
        start = int(re.match(r"\d+", block).group())
        if start != 1:
            props = {"start": start}
    return ParentNode(tag, items, props)


def _quote_to_html(block: str) -> ParentNode:
    quote_text = " ".join(line[1:].lstrip() for line in block.split("\n"))
    return _text_block_to_parent("blockquote", quote_text)


def _code_to_html(block: str) -> ParentNode:
    opening, code_text = block.split("\n", 1)
    fence = opening[:3]
    code_text = code_text[: -len(fence)]
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
        elif block_type == BlockType.THEMATIC_BREAK:
            block_nodes.append(LeafNode("hr", ""))
        else:
            paragraph_text = " ".join(block.split("\n"))
            block_nodes.append(_text_block_to_parent("p", paragraph_text))

    return ParentNode("div", block_nodes)


def extract_title(markdown: str) -> str:
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.CODE:
            continue
        for line in block.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        lines = block.splitlines()
        if len(lines) == 2 and re.fullmatch(r" {0,3}=+[ \t]*", lines[1]):
            return lines[0].strip()
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
        key = key.strip()
        if key in values:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        value = value.strip()
        if any(unicodedata.category(char).startswith("C") for char in value):
            raise ValueError(f"Frontmatter contains control characters: {key}")
        values[key] = value
    if values.get("layout", "page") not in {"home", "page"}:
        raise ValueError("Layout must be home or page")
    return values, content


def normalize_basepath(basepath):
    if any(ord(char) < 32 or ord(char) == 127 for char in basepath):
        raise ValueError("Base path contains control characters")
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
    site_url="https://yaqyn.github.io/folio-static-site",
):
    from html import escape
    from pathlib import Path
    from urllib.parse import quote
    import re

    basepath = normalize_basepath(basepath)
    print(f"Generating {route}")
    metadata, markdown = parse_frontmatter(Path(from_path).read_text(encoding="utf-8"))
    template = Path(template_path).read_text(encoding="utf-8")
    content_node = markdown_to_html_node(markdown)
    # Reserve cover geometry and defer artwork below the fold; the hero stays eager.
    for block in content_node.children:
        for node in block.children or []:
            if node.tag == "img" and node.props["src"].startswith("/images/projects/"):
                static = Path(__file__).resolve().parent.parent / "static"
                image = (static / node.props["src"].lstrip("/")).resolve()
                if not image.is_relative_to(static / "images" / "projects"):
                    raise ValueError("Project cover path must stay inside its asset directory")
                with image.open("rb") as cover:
                    header = cover.read(30)
                if image.suffix.lower() == ".svg":
                    try:
                        svg = ElementTree.parse(image).getroot()
                        width = int(svg.attrib["width"])
                        height = int(svg.attrib["height"])
                        if width <= 0 or height <= 0:
                            raise ValueError("Nonpositive SVG dimensions")
                    except (ElementTree.ParseError, KeyError, ValueError) as error:
                        raise ValueError(
                            "SVG project covers need positive integer width and height"
                        ) from error
                elif header[:8] == b"\x89PNG\r\n\x1a\n":
                    width, height = struct.unpack(">II", header[16:24])
                elif header[:4] == b"RIFF" and header[8:12] == b"WEBP":
                    if header[12:16] == b"VP8X":
                        width = 1 + int.from_bytes(header[24:27], "little")
                        height = 1 + int.from_bytes(header[27:30], "little")
                    elif header[12:16] == b"VP8L" and header[20] == 0x2F:
                        dimensions = int.from_bytes(header[21:25], "little")
                        width = 1 + (dimensions & 0x3FFF)
                        height = 1 + ((dimensions >> 14) & 0x3FFF)
                    else:
                        raise ValueError("Project covers must use lossless WebP")
                else:
                    raise ValueError("Project covers must be PNG, lossless WebP, or SVG images")
                node.props.update(
                    width=str(width), height=str(height), loading="lazy", decoding="async"
                )
    html = content_node.to_html()
    title = extract_title(markdown)
    description = metadata.get(
        "description", f"{title} — projects and notes by Abdulrahman M. Yaqyn."
    )
    layout = metadata.get("layout", "page")
    navigation = []
    for label, target in [
        ("Home", "/"),
        ("Projects", "/projects/"),
        ("Games", "/games/"),
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
        "Canonical": escape(site_url.rstrip("/") + quote(route, safe="/"), quote=True),
        "ImageURL": escape(
            site_url.rstrip("/") + "/images/yaqyn-portrait.webp", quote=True
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
