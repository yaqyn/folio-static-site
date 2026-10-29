from urllib.parse import urlsplit
import unicodedata

from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None, children=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.children = children

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
            and self.children == other.children
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.STRIKETHROUGH:
        return LeafNode("del", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type in {TextType.LINK, TextType.IMAGE}:
        if any(unicodedata.category(char).startswith("C") for char in text_node.url or ""):
            raise ValueError("Link and image URLs cannot contain control characters")
        allowed = {"", "http", "https"}
        if text_node.text_type == TextType.LINK:
            allowed.add("mailto")
        if urlsplit(text_node.url or "").scheme.lower() not in allowed:
            raise ValueError("Unsupported link or image URL scheme")
    if text_node.text_type == TextType.LINK and text_node.children is not None:
        from parentnode import ParentNode

        return ParentNode(
            "a",
            [text_node_to_html_node(child) for child in text_node.children],
            {"href": text_node.url},
        )
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img",
            "",
            {"src": text_node.url, "alt": text_node.text},
        )
    raise ValueError(f"Unsupported text type: {text_node.text_type}")
