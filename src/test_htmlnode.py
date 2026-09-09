import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor_stores_properties(self):
        child = HTMLNode("span", "child")
        node = HTMLNode("div", children=[child], props={"class": "content"})

        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"class": "content"})

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            "a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_with_no_props(self):
        self.assertEqual(HTMLNode("p").props_to_html(), "")
        self.assertEqual(HTMLNode("p", props={}).props_to_html(), "")

    def test_to_html_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode("p", "text").to_html()


if __name__ == "__main__":
    unittest.main()
