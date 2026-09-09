import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splits_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_splits_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_splits_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_preserves_non_text_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([bold_node], "`", TextType.CODE),
            [bold_node],
        )

    def test_splits_multiple_text_nodes(self):
        nodes = [
            TextNode("first `code`", TextType.TEXT),
            TextNode("second text", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("first ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("second text", TextType.TEXT),
            ],
        )

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This has an unmatched ` delimiter", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Unmatched delimiter"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_segments_are_omitted(self):
        node = TextNode("`code`", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("code", TextType.CODE)],
        )


if __name__ == "__main__":
    unittest.main()
