import re

from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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
            new_nodes.append(TextNode(label, text_type, url))

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


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
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
