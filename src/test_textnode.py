import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertIsNone(node.url)
        self.assertEqual(node, TextNode("plain text", TextType.TEXT, None))

    def test_different_text_type_is_not_equal(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_text_is_not_equal(self):
        node = TextNode("first text", TextType.TEXT)
        node2 = TextNode("second text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_different_url_is_not_equal(self):
        node = TextNode("link", TextType.LINK, "https://example.com/one")
        node2 = TextNode("link", TextType.LINK, "https://example.com/two")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
