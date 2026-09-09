import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_without_tag_returns_raw_text(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_empty_string_is_a_valid_value(self):
        self.assertEqual(LeafNode("p", "").to_html(), "<p></p>")


if __name__ == "__main__":
    unittest.main()
