import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        self.assertEqual(
            markdown_to_html_node("### A heading").to_html(),
            "<div><h3>A heading</h3></div>",
        )

    def test_quote(self):
        markdown = "> first line\n> second line"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><blockquote>first line second line</blockquote></div>",
        )

    def test_unordered_list(self):
        markdown = "- first item\n- **bold** item"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ul><li>first item</li><li><b>bold</b> item</li></ul></div>",
        )

    def test_ordered_list(self):
        markdown = "1. first item\n2. second item"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ol><li>first item</li><li>second item</li></ol></div>",
        )

    def test_links_and_images(self):
        markdown = "A [link](https://example.com) and ![image](image.png)"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            '<div><p>A <a href="https://example.com">link</a> and '
            '<img src="image.png" alt="image"></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
