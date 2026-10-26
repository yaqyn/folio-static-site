![Folio — yaqyn’s portrait-led charcoal portfolio](readme-assets/site-preview.webp)

# Folio — Personal Site & Generator

**Abdulrahman M. Yaqyn's projects and development notes, powered by a small Python static site generator.**

Folio brings together three career projects, two personal projects, twelve Boot.dev learning projects, and development notes. The site uses a charcoal palette and an original black-and-white author portrait. Its Python generator turns Markdown into the pages you see, including the full project inventory, games page, biography, contact page, workflow and technical notes, and custom 404 page.

[Visit the published site](https://yaqyn.github.io/folio-static-site/) · [Run locally](#-quick-start) · [Design context](DESIGN.md)

## <img src="readme-assets/icons/features.svg" width="24" height="24" alt=""> Features

- Turn Markdown into linked static pages with a shared template.
- Explore career, personal, and learning projects with source links.
- Read development notes and navigate the site without JavaScript.
- Build pages in a temporary stage before replacing published output.

## <img src="readme-assets/icons/installation.svg" width="24" height="24" alt=""> Installation

Requires **Python 3.10+**. No third-party runtime dependencies.

Clone with `git clone https://github.com/yaqyn/folio-static-site.git`, then run the commands below from `folio-static-site/`.

## <img src="readme-assets/icons/launch.svg" width="24" height="24" alt=""> Quick start

```bash
./launch
```

Open **http://127.0.0.1:8888**. The launcher builds a local version and serves it on the loopback interface. Stop with **Ctrl+C**. Use `./launch 8891` for another port. It works from any directory when invoked by absolute path; `sh main.sh` remains an alias.

## <img src="readme-assets/icons/usage.svg" width="24" height="24" alt=""> Usage

| Location | Purpose |
| --- | --- |
| `content/` | Markdown pages and development notes |
| `static/` | Shared styles, favicon, and the original author portrait |
| `template.html` | Navigation, landmarks, metadata, and footer |
| `src/` | Parser, HTML tree, staged build, and tests |
| `docs/` | Generated output used by GitHub Pages |

Markdown supports headings, paragraphs, quotes, `-`, `*`, and `+` unordered lists (plus custom ordered-list starts), thematic breaks, links, images, bold, italics, inline code, and fenced code with optional language labels. Blank lines inside code fences are preserved. Raw HTML is escaped rather than executed. Project-cover dimensions are read from PNG, lossless WebP, and canonical SVG files with positive integer width and height. Covers load lazily with their geometry reserved; the homepage portrait stays eager.

Pages may start with a small frontmatter block:

```markdown
---
description: A useful one-sentence page description.
layout: page
---
# Page title
```

Supported keys are `description` and `layout`; layouts are `page` and `home`. This is a deliberately small key-value format, not a full YAML parser. The homepage's first three paragraphs are its introduction, actions, and image. Keep that order when editing its content.

Build for the existing GitHub Pages project path:

```bash
sh build.sh
```

Or choose another base path, output, and canonical public URL:

```bash
python3 src/main.py /portfolio/ --output /tmp/portfolio --site-url https://example.com/portfolio
```

Builds stage assets and pages in a temporary directory before replacing generated output. A broken Markdown page leaves the previous build intact. Existing custom output directories need a `.nojekyll` marker; the generator protects the project, source, and Git directories. Edit sources rather than generated HTML. Regenerate `docs/` with `sh build.sh` before committing for publication.

Local links receive the selected base path; external and protocol-relative links retain their destinations. Text and attributes are HTML-escaped, and unsupported link/image schemes are rejected. Every page has a description, canonical URL, social metadata, and selected navigation.

## <img src="readme-assets/icons/projects.svg" width="24" height="24" alt=""> Projects

### <img src="readme-assets/icons/career.svg" width="20" height="20" alt=""> Career projects

![HyperQuote — Build the Future, Faster.](static/images/hyperquote-cover.gif)

| Project | Purpose |
| --- | --- |
| [HyperQuote](https://github.com/yaqyn/HyperQuote) | Connected procurement and delivery workflows; public showcase |
| [Modern](https://github.com/yaqyn/Modern) | Bilingual construction-company website; public showcase |
| Stockroom | Private warehouse evaluation prototype |

Application source stays private. [Yaqyn Development](https://github.com/yaqyn-dev) introduces the career projects and development workflow.

### <img src="readme-assets/icons/projects.svg" width="20" height="20" alt=""> Personal projects

![qvOS — Personal Linux Distribution](static/images/qvos-cover.gif)

| Project | Purpose |
| --- | --- |
| [qvOS](https://github.com/yaqyn/qvOS) | Standalone Arch Linux distribution in active development |
| [Counter](https://github.com/yaqyn/omarchy-counter) | Native Omarchy tally counter |

### <img src="readme-assets/icons/learning.svg" width="20" height="20" alt=""> Learning journey projects

Twelve projects exploring private notes, link workspaces, APIs, services, retrieval, terminal interfaces, games, and static publishing.

| Project | Purpose |
| --- | --- |
| [Leafmark](https://github.com/yaqyn/leafmark-notebook) | Private plain-text notebook with exportable drafts |
| [Waymark](https://github.com/yaqyn/waymark-link-shortener) | Editable short links and request observability |
| [Readlane](https://github.com/yaqyn/readlane-feed-reader) | Terminal-first RSS and Atom Reader |
| [Clibble](https://github.com/yaqyn/clibble-terminal-rpg) | Original Offline Terminal RPG |
| [Threadline](https://github.com/yaqyn/threadline-social-api) | Social Publishing API |
| [Portlight](https://github.com/yaqyn/portlight-http-server) | Containerized HTTP Server |
| [Workbench](https://github.com/yaqyn/workbench-ai-agent) | AI Coding Agent |
| [CineSearch](https://github.com/yaqyn/cinesearch-rag-engine) | Movie RAG Engine |
| [SiteLens](https://github.com/yaqyn/sitelens-web-crawler) | Web Crawler |
| [Orbit](https://github.com/yaqyn/orbit-asteroids-game) | Asteroids Game |
| [TextScope](https://github.com/yaqyn/textscope-text-analyzer) | Text Analyzer |
| [Folio](https://github.com/yaqyn/folio-static-site) | Personal Site & Generator |

## <img src="readme-assets/icons/architecture.svg" width="24" height="24" alt=""> Architecture

The parser builds text nodes, converts them into an HTML tree, and renders pages through a shared template. The build stages pages and static assets before replacing the output directory.

![Markdown-to-page workflow](readme-assets/workflow.svg)

[Read the implementation notes](content/notes/static-sites/index.md).

## <img src="readme-assets/icons/verification.svg" width="24" height="24" alt=""> Verification

```bash
sh test.sh
```

The unittest suite covers parsing, HTML nodes, page generation, frontmatter, escaping, link schemes, code fences, all local routes and assets, and recovery from a failed build. It also checks intrinsic geometry and lazy loading for the vector and raster project covers. GitHub Actions tests Python 3.10 and 3.13 and checks that the published build is reproducible.

The responsive theme has been checked in an isolated Chromium browser at desktop, 390px, and 320px widths, including keyboard skip navigation, project/note links, reduced motion, and the 404 recovery page. The site uses no JavaScript or remote fonts.

---

Built by **[Abdulrahman M. Yaqyn](https://github.com/yaqyn)**.

> **Learning Journey Project · Boot.dev**
> Built through the Boot.dev curriculum and extended into my personal portfolio.
