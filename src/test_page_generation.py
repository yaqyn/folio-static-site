import tempfile
import unittest
from pathlib import Path

from markdown_to_html import extract_title, generate_page


class TestPageGeneration(unittest.TestCase):
    def test_canonical_route_is_url_encoded_before_html_escaping(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, template, output = root / "page.md", root / "template.html", root / "page.html"
            source.write_text("# Test")
            template.write_text('<link rel="canonical" href="{{ Canonical }}">')
            generate_page(source, template, output, route="/notes/café #1.html", site_url="https://example.com")
            self.assertIn('href="https://example.com/notes/caf%C3%A9%20%231.html"', output.read_text())

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Hello world  "), "Hello world")

    def test_extract_title_requires_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Only a subheading")

    def test_extract_title_ignores_code_examples(self):
        self.assertEqual(extract_title("```markdown\n# Example\n```\n\n# Actual title"), "Actual title")
        with self.assertRaises(ValueError):
            extract_title("```\n# Not a heading\n```")

    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.md"
            template = root / "template.html"
            destination = root / "nested" / "index.html"
            source.write_text("# Test page\n\nHello **world**")
            template.write_text("<title>{{ Title }}</title>{{ Content }}")

            generate_page(str(source), str(template), str(destination))

            self.assertEqual(
                destination.read_text(),
                "<title>Test page</title><div><h1>Test page</h1>"
                "<p>Hello <b>world</b></p></div>",
            )

    def test_generate_page_with_basepath(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.md"
            template = root / "template.html"
            destination = root / "index.html"
            source.write_text("# Test page\n\n[Home](/)")
            template.write_text("{{ Title }}{{ Content }}")

            generate_page(str(source), str(template), str(destination), "/folio-static-site/")

            self.assertIn('href="/folio-static-site/"', destination.read_text())


if __name__ == "__main__":
    unittest.main()
