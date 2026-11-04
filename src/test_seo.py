from contextlib import redirect_stdout
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree

from main import build_site
from seo import page_metadata


class Metadata(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta, self.links, self.title, self.structured = {}, {}, '', ''
        self.in_title = self.in_json = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        elif tag == 'link':
            self.links.setdefault(attrs.get('rel'), []).append(attrs.get('href'))
        elif tag == 'title':
            self.in_title = True
        elif tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_json = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.in_json = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_json:
            self.structured += data


class SEOTests(unittest.TestCase):
    def test_structured_data_cannot_close_its_script_element(self):
        title = '</script><script>alert("x")</script> & text'
        result = page_metadata(title, title, '/notes/test/', 'https://example.com')
        self.assertNotIn('<', result['StructuredData'])
        graph = json.loads(result['StructuredData'])['@graph']
        self.assertEqual(graph[2]['name'], title)
        self.assertEqual(graph[-1]['itemListElement'][-1]['name'], title)

    def test_deployment_metadata_sitemap_and_error_indexing(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = build_site(output=Path(directory)/'site')
            namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            sitemap = ElementTree.parse(root/'sitemap.xml')
            urls = [node.text for node in sitemap.findall('s:url/s:loc', namespace)]
            self.assertEqual(len(urls), 9)
            self.assertNotIn('https://yaqyn.dev/404.html', urls)
            self.assertIn('https://yaqyn.dev/sitemap.xml', (root/'robots.txt').read_text())
            titles = set()
            for page in root.rglob('*.html'):
                data = Metadata(page.read_text())
                self.assertTrue(data.title)
                self.assertNotIn(data.title, titles)
                titles.add(data.title)
                self.assertEqual(data.meta['og:title'], data.title)
                self.assertEqual(data.meta['twitter:title'], data.title)
                self.assertEqual(data.meta['og:image:width'], '1200')
                self.assertEqual(data.meta['og:image:height'], '630')
                self.assertTrue((root/'icon-192.png').is_file())
                self.assertIn('/favicon.svg', data.links['icon'])
                canonical = data.links['canonical'][0]
                if page.name == '404.html':
                    self.assertEqual(data.meta['robots'], 'noindex, follow')
                else:
                    self.assertIn(canonical, urls)
                    graph = json.loads(data.structured)['@graph']
                    self.assertEqual(graph[2]['url'], canonical)
                    self.assertIn('index, follow', data.meta['robots'])
            home = Metadata((root/'index.html').read_text())
            self.assertIn('Abdulrahman M. Yaqyn', home.title)
            self.assertIn('Backend', home.title)

    def test_custom_host_is_used_everywhere_in_generated_search_files(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = build_site('/folio/', Path(directory)/'site', 'https://example.com/folio')
            html = (root/'games/index.html').read_text()
            data = Metadata(html)
            self.assertEqual(data.links['canonical'], ['https://example.com/folio/games/'])
            self.assertEqual(data.meta['og:image'], 'https://example.com/folio/images/social-card.webp')
            self.assertIn('https://example.com/folio/sitemap.xml', (root/'robots.txt').read_text())
            self.assertNotIn('https://yaqyn.dev', (root/'sitemap.xml').read_text())
            self.assertIn('/folio/icon-192.png', data.links['icon'])
            home = (root/'index.html').read_text()
            self.assertIn('srcset="/folio/images/yaqyn-portrait-384.webp 384w, ', home)
            self.assertIn('fetchpriority="high"', home)
            self.assertTrue((root/'images/yaqyn-portrait-384.webp').exists())
