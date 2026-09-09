import unittest

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_converts_mixed_markdown(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("plain text"),
            [TextNode("plain text", TextType.TEXT)],
        )

    def test_single_inline_type(self):
        self.assertEqual(
            text_to_textnodes("before **bold** after"),
            [
                TextNode("before ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_inline_elements_at_boundaries(self):
        self.assertEqual(
            text_to_textnodes("**bold**`code`"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode("code", TextType.CODE),
            ],
        )


if __name__ == "__main__":
    unittest.main()
