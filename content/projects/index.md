---
description: Career applications, independent Linux tools, and twelve Boot.dev projects by Abdulrahman M. Yaqyn. Explore the behavior, engineering choices, and source.
---
# Projects

Client applications, independent tools, and twelve learning projects. Career work has approved public showcases; personal and learning projects link to their source and run instructions. Private prototypes are identified as such.

## Career projects

![HyperQuote — Build the Future, Faster.](/images/hyperquote-cover.gif)

### HyperQuote — Connected Business Operations

A building-materials procurement platform connecting customers, sales, internal operations, management, dispatch, and drivers, from a material request to delivery.

- Connected orders, inventory, suppliers, warehousing, fleet, finance, and customer-service workflows.
- Natural-language ordering and a RAG-based assistant for accessing company information.
- Customer, operations, and driver experiences around shared data and coordinated handoffs.

**Stack:** TypeScript, React, TanStack Start, Supabase, PostgreSQL, Cloudflare Workers, and Infisical.

Application source and deployment configuration remain private. The public showcase uses fictional data and shared demonstration accounts.

[Explore HyperQuote](https://github.com/yaqyn/HyperQuote), [visit the website](https://www.hyperquote.net), or [open the customer portal](https://portal.hyperquote.net).

### Modern — Construction company website

![Modern — green brand mark and descending architectural forms](/images/projects/modern-cover.webp)

A bilingual website for Modern Construction for Contracting. Visitors can explore services, filter project galleries, and carry service or project context into a structured inquiry. English and Arabic layouts support both reading directions and light/dark themes.

**Stack:** TypeScript, React, TanStack Start, Tailwind CSS, i18next, and Cloudflare Workers.

The public repository presents selected interface captures; application source stays private. The materials marketplace remains in preparation. The cover is illustrative brand artwork.

[Explore the Modern showcase](https://github.com/yaqyn/Modern) or [visit the website](https://www.moderngroupco.com/).

### Stockroom — Warehouse workflow prototype

A private, local evaluation prototype for barcode-guided receiving, storage-place suggestions, and internal transfers. A suggestion leaves stock unchanged; confirmation rechecks capacity and contents, then records the balance change and its history together. Request identifiers protect unchanged retries from duplicate movements.

**Current implementation:** Python, SQLite, and browser JavaScript.

Authentication, Odoo integration, and production operation are outside the current prototype. Source and internal materials remain private.

[Read the career-project gallery](https://github.com/yaqyn-dev#stockroom) for public context on Stockroom and the development workflow.

## Personal projects

![qvOS — Personal Linux Distribution](/images/qvos-cover.gif)

### qvOS — Personal Linux Distribution

A standalone Arch Linux distribution in active development. qvOS maintains its own keyboard-first Hyprland desktop, native system tools, installer, and release lifecycle. Daily use guides decisions about development, updates, and recovery.

Public ISO downloads are not available yet; the repository documents source builds and release checks.

**Focus:** Arch Linux, Hyprland, command-line tools, desktop integration, and automation.

[Explore qvOS](https://github.com/yaqyn/qvOS) or [read about its architecture](https://github.com/yaqyn/qvOS/blob/OS/qvcore/README.md).

Package foundation: Omarchy’s signed Stable repositories, distributed through Cloudflare, support the focus on stability.

### Counter — Quiet counting in Omarchy

![Counter — a tally display connected to a counting key](/images/projects/counter-cover.svg)

A chosen key adds one count without switching windows, opening a panel, or repeatedly counting when held. The Omarchy bar displays the number; its native panel provides Reset, Undo, and a key chooser. The total and selected key persist across restarts, and shortcut checks protect existing bindings.

**Stack:** Python, QML, Quickshell, and Hyprland.

Built for Omarchy's native plugin system. It follows the desktop theme and requires supported Omarchy, Hyprland, and Quickshell versions.

[Explore Counter on GitHub](https://github.com/yaqyn/omarchy-counter).

## Learning journey projects

**Projects developed through the Boot.dev curriculum and extended through independent work.**

Orbit and Clibble have complete entries on the [Games page](/games/).

### Leafmark — Personal notebook

![Leafmark — a page of your own](/images/projects/leafmark-cover.svg)

A private, plain-text notebook with search, pinned notes, archives, Trash, and JSON or Markdown exports. Revocable cookie sessions protect accounts; revision checks reject stale saves, and a failed save still leaves the draft available to download.

**Stack:** Go, browser JavaScript, SQLite, and optional Turso.

Local SQLite needs no external account. Production hosting requires HTTPS, durable storage, backups, and registration controls. Leafmark extends Boot.dev's CI/CD starter and the earlier Notely application.

[Explore Leafmark on GitHub](https://github.com/yaqyn/leafmark-notebook).

### Waymark — Private link workspace

![Waymark — a route marker over an ink-blue landscape](/images/projects/waymark-cover.webp)

Create recognizable short addresses, update destinations, schedule expiration, and inspect persistent click totals. The Go server embeds the browser interface and stores records on disk. Structured request logs, Prometheus metrics, optional traces, and development profiles make server behavior inspectable.

Designed for one trusted account and one running process per data directory. Click totals count served redirects, not unique visitors. Production requires configured credentials and HTTPS.

[Explore Waymark on GitHub](https://github.com/yaqyn/waymark-link-shortener) or [follow a request through its observability stack](https://github.com/yaqyn/waymark-link-shortener/blob/main/docs/observability.md).

### Readlane — Feed Reader

![Readlane — Feed Reader](/images/projects/readlane-cover.webp)

A terminal-first RSS and Atom reader with PostgreSQL-backed collection. Follow sources, search collected posts, and read summaries with the keyboard. A single collection worker uses cache validators and persistent retry backoff; an optional read-only web companion displays the same stories. Reader selection assumes a trusted local environment and is not authentication.

[Explore Readlane on GitHub](https://github.com/yaqyn/readlane-feed-reader)


### Clibble — Terminal RPG

An offline forest adventure with original wildlings, a persistent field journal, and saved catch limits. The terminal interface has keyboard selection and optional motion; a local read-only web companion lets you explore the journal.

[Explore Clibble on the Games page](/games/) or [open its source](https://github.com/yaqyn/clibble-terminal-rpg).

### Threadline — Social Publishing API

![Threadline — Social Publishing API](/images/projects/threadline-cover.webp)

A Go and PostgreSQL backend for short-form publishing, with Argon2id password hashing, signed access tokens, revocable refresh sessions, author-owned posts, and membership webhooks. OpenAPI documentation and regression tests describe the HTTP contract.

[Explore Threadline on GitHub](https://github.com/yaqyn/threadline-social-api)

### Portlight — HTTP Server

![Portlight — HTTP Server](/images/projects/portlight-cover.webp)

A small Go HTTP service packaged in a minimal non-root Docker image. Validated startup configuration, health probes, JSON request logs, connection timeouts, and graceful shutdown make the operating behavior explicit.

[Explore Portlight on GitHub](https://github.com/yaqyn/portlight-http-server)

### Workbench — AI Coding Agent

![Workbench — AI Coding Agent](/images/projects/workbench-cover.webp)

A full-screen terminal coding workbench using OpenRouter. Inspect a project, edit files, and run Python through workspace-scoped tools. Sessions begin in Inspect only mode; settings, bounded runs, themes, and saved transcripts make behavior reviewable. An offline preview needs no credentials. Model requests require an OpenRouter key, and Python execution runs on the host rather than in an operating-system sandbox.

[Explore Workbench on GitHub](https://github.com/yaqyn/workbench-ai-agent)

### CineSearch — Movie RAG Engine

![CineSearch — Movie RAG Engine](/images/projects/cinesearch-cover.webp)

A keyboard-driven movie browser and RAG engine combining BM25 keyword scoring, semantic embeddings, chunk retrieval, hybrid ranking, reranking, and grounded generation. Cover-inspired and high-contrast terminal themes sit alongside a plain-text mode. Evaluation commands measure retrieval against a golden dataset. Keyword and semantic search run locally; LLM-powered commands use OpenRouter and require your own API key.

[Explore CineSearch on GitHub](https://github.com/yaqyn/cinesearch-rag-engine)

### SiteLens — Web Crawler

![SiteLens — Web Crawler](/images/projects/sitelens-cover.webp)

A keyboard-driven terminal workspace for bounded, asynchronous crawling. Choose a preset, follow live progress, and collect headings, links, images, and representative paragraphs. A fixed worker pool, robots.txt checks, request limits, deterministic output, and atomic report writes make runs inspectable. Crawl failures stay separate from successful page data.

[Explore SiteLens on GitHub](https://github.com/yaqyn/sitelens-web-crawler)


### Orbit — Asteroids game

An upgradeable starfighter, rotating asteroid meshes, salvage, shields, and escalating contracts. A logical game canvas supports resizable and fullscreen play while preserving the field's proportions.

[Explore Orbit on the Games page](/games/) or [open its source](https://github.com/yaqyn/orbit-asteroids-game).

### TextScope — Text Analyzer

![TextScope — Text Analyzer](/images/projects/textscope-cover.webp)

A dependency-free text-analysis tool with a book picker, a terminal dashboard, vocabulary charts, comparisons, and text, JSON, or CSV exports. Cover-inspired, paper, high-contrast, and terminal-default themes support different reading environments. Plain output remains available for linear reading and pipelines; report writes are atomic and cannot overwrite an input book.

[Explore TextScope on GitHub](https://github.com/yaqyn/textscope-text-analyzer)

### Folio — Personal Site & Generator

![Folio — Personal Site & Generator](/images/projects/folio-cover.webp)

A static site generator written in Python. It turns Markdown into a linked website using a shared template and a small HTML-node model.

[Read how the site works](/notes/static-sites/) or [explore the source](https://github.com/yaqyn/folio-static-site).
