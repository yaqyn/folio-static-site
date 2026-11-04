"""Search metadata built from the same public pages and canonical site URL."""
import json
from urllib.parse import quote
from xml.etree import ElementTree

NAME = "Abdulrahman M. Yaqyn"


def page_metadata(title, description, route, site_url, seo_title=None):
    origin = site_url.rstrip("/")
    canonical = origin + quote(route, safe="/")
    person_id, site_id = origin + "/#person", origin + "/#website"
    page_type = {
        "/about/": "AboutPage", "/contact/": "ContactPage",
        "/projects/": "CollectionPage", "/games/": "CollectionPage",
        "/notes/": "CollectionPage",
    }.get(route, "WebPage")
    graph = [
        {"@type": "Person", "@id": person_id, "name": NAME,
         "alternateName": ["yaqyn", "yaqyndev"], "url": origin + "/about/",
         "image": origin + "/images/yaqyn-portrait.webp",
         "sameAs": [
             "https://github.com/yaqyn",
             "https://linkedin.com/in/yaqyn",
             "https://bsky.app/profile/yaqyn.dev",
             "https://www.patreon.com/cw/yaqyn",
             "https://www.youtube.com/@yaqyndev",
             "https://gravatar.com/yaqyndev",
             "https://x.com/yaqyndev",
             "https://yaqyndev.contra.com/",
             "https://t.me/yaqyndev",
             "https://www.boot.dev/u/yaqyn",
         ]},
        {"@type": "WebSite", "@id": site_id, "name": "yaqyn",
         "alternateName": NAME, "url": origin + "/", "inLanguage": "en",
         "publisher": {"@id": person_id}},
        {"@type": page_type, "@id": canonical + "#page", "url": canonical,
         "name": seo_title or title, "description": description,
         "isPartOf": {"@id": site_id}, "inLanguage": "en",
         "author": {"@id": person_id}},
    ]
    if route != "/" and route != "/404.html":
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": origin + "/"}]
        if route.startswith("/notes/") and route != "/notes/":
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Notes", "item": origin + "/notes/"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs)+1, "name": title, "item": canonical})
        graph.append({"@type": "BreadcrumbList", "@id": canonical + "#breadcrumbs", "itemListElement": crumbs})
        graph[2]["breadcrumb"] = {"@id": canonical + "#breadcrumbs"}
    if route == "/about/":
        graph[2]["mainEntity"] = {"@id": person_id}
    # JSON-LD lives in an HTML script element. Escape HTML delimiters even when
    # page titles contain markup-like text; JSON parsing restores those characters.
    structured = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    for char, escaped in [("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e")]:
        structured = structured.replace(char, escaped)
    return {
        "DocumentTitle": seo_title or f"{title} | {NAME}",
        "Robots": "noindex, follow" if route == "/404.html" else "index, follow, max-image-preview:large",
        "StructuredData": structured if route != "/404.html" else "{}",
    }


def write_crawl_files(output, site_url):
    """List real generated pages, excluding the error page and invented dates."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    sitemap = ElementTree.Element(f"{{{namespace}}}urlset")
    for page in sorted(output.rglob("*.html")):
        route = "/" + page.relative_to(output).as_posix()
        if route == "/404.html":
            continue
        if route.endswith("index.html"):
            route = route[:-len("index.html")]
        entry = ElementTree.SubElement(sitemap, f"{{{namespace}}}url")
        ElementTree.SubElement(entry, f"{{{namespace}}}loc").text = site_url.rstrip("/") + quote(route, safe="/")
    ElementTree.ElementTree(sitemap).write(output/"sitemap.xml", encoding="utf-8", xml_declaration=True)
    (output/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: " + site_url.rstrip("/") + "/sitemap.xml\n")
