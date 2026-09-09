import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extracts_multiple_images(self):
        text = (
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_links_do_not_include_images(self):
        text = "![image](image.png) and [link](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")],
        )

    def test_empty_alt_and_anchor_text_are_allowed(self):
        self.assertEqual(
            extract_markdown_images("![](image.png)"),
            [("", "image.png")],
        )
        self.assertEqual(
            extract_markdown_links("[](https://example.com)"),
            [("", "https://example.com")],
        )

    def test_no_matches_returns_empty_list(self):
        self.assertEqual(extract_markdown_images("plain text"), [])
        self.assertEqual(extract_markdown_links("plain text"), [])


if __name__ == "__main__":
    unittest.main()
