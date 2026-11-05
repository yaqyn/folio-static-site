import re

from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)", text)


def _split_nodes_by_markdown(
    old_nodes: list[TextNode],
    extractor,
    text_type: TextType,
    marker_prefix: str,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extractor(remaining_text)
        if not matches:
            if remaining_text:
                new_nodes.append(old_node)
            continue

        for label, url in matches:
            markdown = f"{marker_prefix}[{label}]({url})"
            sections = remaining_text.split(markdown, 1)
            if len(sections) != 2:
                continue

            before, remaining_text = sections
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            children = None
            title = None
            if text_type == TextType.LINK:
                titled = re.fullmatch(r"(.+?)[ \t]+(['\"])(.*?)\2", url)
                if titled:
                    url, title = titled.group(1), titled.group(3)
                parsed_label = text_to_textnodes(label)
                if any(node.text_type != TextType.TEXT for node in parsed_label):
                    children = parsed_label
            new_nodes.append(TextNode(label, text_type, url, children, title))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown(
        old_nodes, extract_markdown_images, TextType.IMAGE, "!"
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown(
        old_nodes, extract_markdown_links, TextType.LINK, ""
    )


def split_nodes_autolink(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    pattern = re.compile(r"<(https?://[^<>\s]+|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)>")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        position = 0
        for match in pattern.finditer(node.text):
            if match.start() > position:
                new_nodes.append(TextNode(node.text[position:match.start()], TextType.TEXT))
            url = match.group(1)
            destination = url if url.startswith(("http://", "https://")) else f"mailto:{url}"
            new_nodes.append(TextNode(url, TextType.LINK, destination))
            position = match.end()
        if position < len(node.text):
            new_nodes.append(TextNode(node.text[position:], TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    escapes = {"\\*": "\ue000", "\\_": "\ue001", "\\~": "\ue002", "\\`": "\ue003"}
    for escaped, placeholder in escapes.items():
        text = text.replace(escaped, placeholder)
    text = re.sub(r"(?<=[^\W_])_(?=[^\W_])", "\ue004", text)
    nodes = [TextNode(text, TextType.TEXT)]
    # Code spans are literal: protect their contents before interpreting
    # links, images, or emphasis delimiters.
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_autolink(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKETHROUGH)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    restore = {placeholder: escaped[1:] for escaped, placeholder in escapes.items()}
    restore["\ue004"] = "_"
    for node in nodes:
        for placeholder, literal in restore.items():
            node.text = node.text.replace(placeholder, literal)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: {delimiter}")

        for index, part in enumerate(parts):
            if part == "":
                continue
            node_type = text_type if index % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))

    return new_nodes
