from contextlib import redirect_stdout
from html.parser import HTMLParser
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit, unquote

from leafnode import LeafNode
from htmlnode import HTMLNode
from markdown_to_html import (
    generate_page,
    markdown_to_html_node,
    normalize_basepath,
    parse_frontmatter,
)
from main import build_site, ROOT


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(
            value for key, value in attrs if key in {"href", "src"} and value
        )


class TestSiteReliability(unittest.TestCase):
    def test_html_text_and_attributes_are_escaped(self):
        self.assertEqual(
            LeafNode("code", "<script>&").to_html(), "<code>&lt;script&gt;&amp;</code>"
        )
        self.assertEqual(
            HTMLNode(props={"alt": '" & <'}).props_to_html(), ' alt="&quot; &amp; &lt;"'
        )
        self.assertIn(
            "&lt;script&gt;", markdown_to_html_node("# Hi\n\n<script>").to_html()
        )

    def test_unsafe_link_schemes_are_rejected(self):
        for markdown in [
            "[link](javascript:alert)",
            "![image](data:text/html,evil)",
            "[link](vbscript:evil)",
        ]:
            with self.subTest(markdown=markdown), self.assertRaises(ValueError):
                markdown_to_html_node(markdown)

    def test_code_fences_preserve_blank_lines_and_language(self):
        result = markdown_to_html_node(
            '# Code\n\n```python\nx = "<tag>"\n\nprint(x)\n```'
        ).to_html()
        self.assertIn(
            '<code class="language-python">x = "&lt;tag&gt;"\n\nprint(x)\n</code>',
            result,
        )

    def test_unclosed_code_fence_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, "Unclosed fenced"):
            markdown_to_html_node("# Code\n\n```\nincomplete")

    def test_frontmatter(self):
        metadata, content = parse_frontmatter(
            "---\nlayout: home\ndescription: Custom copy\n---\n# Test"
        )
        self.assertEqual(metadata, {"layout": "home", "description": "Custom copy"})
        self.assertEqual(content, "# Test")
        for markdown in [
            "---\nlayout: home",
            "---\nunknown: value\n---\n# Test",
            "---\nlayout: invalid\n---\n# Test",
        ]:
            with self.subTest(markdown=markdown), self.assertRaises(ValueError):
                parse_frontmatter(markdown)

    def test_basepath_normalization(self):
        self.assertEqual(normalize_basepath("/folio-static-site"), "/folio-static-site/")
        self.assertEqual(normalize_basepath("/"), "/")
        for path in ["relative", "/../", "/a/../b", '/bad"', "/bad?query"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                normalize_basepath(path)

    def test_template_metadata_is_not_reinterpreted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, template, destination = [
                root / name for name in ["page.md", "template.html", "page.html"]
            ]
            source.write_text(
                "# A & B\n\n{{ Description }}\n\n[External](//example.com/image)"
            )
            template.write_text("<title>{{ Title }}</title>{{ Content }}")
            generate_page(source, template, destination, "/site/")
            result = destination.read_text()
            self.assertIn("<title>A &amp; B</title>", result)
            self.assertIn("{{ Description }}", result)
            self.assertIn('href="//example.com/image"', result)

    def test_all_local_routes_and_assets_exist(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            output = build_site("/folio-static-site", Path(directory) / "site")
            pages = list(output.rglob("*.html"))
            self.assertEqual(len(pages), 8)
            for page in pages:
                markup = page.read_text()
                self.assertNotIn("Tolkien", markup)
                self.assertIn('<html lang="en">', markup)
                links = Links()
                links.feed(markup)
                for url in links.urls:
                    if url.startswith("/folio-static-site/"):
                        local = output / unquote(
                            urlsplit(url).path.removeprefix("/folio-static-site/")
                        )
                        if local.is_dir():
                            local /= "index.html"
                        self.assertTrue(local.exists(), f"{page}: missing {url}")
            self.assertTrue((output / ".nojekyll").exists())
            self.assertIn(
                'aria-current="page">Projects',
                (output / "projects/index.html").read_text(),
            )

    def test_failed_build_preserves_previous_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "site"
            output.mkdir()
            (output / ".nojekyll").touch()
            (output / "index.html").write_text("previous")
            with patch(
                "main.generate_pages_recursive",
                side_effect=ValueError("broken markdown"),
            ):
                with self.assertRaises(ValueError):
                    build_site("/", output)
            self.assertEqual((output / "index.html").read_text(), "previous")

    def test_output_guards_source_and_unknown_directories(self):
        for output in [ROOT, ROOT / "content", ROOT / ".git", ROOT / "static/images"]:
            with self.subTest(output=output), self.assertRaises(ValueError):
                build_site("/", output)
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            build_site("/", Path(directory))
