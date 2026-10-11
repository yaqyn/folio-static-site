---
description: Software and systems projects by Abdulrahman M. Yaqyn, from qvOS to Python tools and games.
---
# Projects

My work has three distinct parts: career projects, personal projects, and student projects documenting my learning journey. Each project links to its source.

## Career Projects

![HyperQuote — Build the Future, Faster.](/images/hyperquote-cover.gif)

### HyperQuote — Connected Business Operations

A building-materials procurement platform connecting customers, sales, internal operations, management, dispatch, and drivers, from a material request to delivery.

- Connected orders, inventory, suppliers, warehousing, fleet, finance, and customer-service workflows.
- Natural-language ordering and a RAG-based assistant for accessing company information.
- Customer, operations, and driver experiences around shared data and coordinated handoffs.

**Stack:** TypeScript, React, TanStack Start, Supabase, PostgreSQL, Cloudflare Workers, and Infisical.

[Explore HyperQuote](https://github.com/yaqyn/HyperQuote), [visit the website](https://www.hyperquote.net), or [open the customer portal](https://portal.hyperquote.net).

## Personal Projects

![qvOS — Personal Linux Distribution](/images/qvos-cover.gif)

### qvOS — Personal Linux Distribution

An ongoing standalone Arch Linux distribution project, originally built on Omarchy. A keyboard-first Hyprland desktop, native system tools, installation, updates, and recovery, adapted around my development, productivity, automation, and AI agent workflows.

**Focus:** Arch Linux, Hyprland, command-line tools, desktop integration, and automation.

[Explore qvOS](https://github.com/yaqyn/qvOS) or [read about its architecture](https://github.com/yaqyn/qvOS/blob/OS/qvcore/README.md)

## Learning Journey Projects

**Student projects developed through the Boot.dev curriculum and extended through hands-on practice.**

### Threadline — Social Publishing API

![Threadline — Social Publishing API](/images/projects/threadline-cover.png)

A Go and PostgreSQL backend for short-form publishing, with Argon2id password hashing, signed access tokens, revocable refresh sessions, author-owned posts, and membership webhooks. OpenAPI documentation and regression tests describe the HTTP contract.

[Explore Threadline on GitHub](https://github.com/yaqyn/threadline-social-api)

### Portlight — HTTP Server

![Portlight — HTTP Server](/images/projects/portlight-cover.png)

A small Go HTTP service packaged in a minimal non-root Docker image. Validated startup configuration, health probes, JSON request logs, connection timeouts, and graceful shutdown make the operating behavior explicit.

[Explore Portlight on GitHub](https://github.com/yaqyn/portlight-http-server)

### Workbench — AI Coding Agent

![Workbench — AI Coding Agent](/images/projects/workbench-cover.png)

A command-line coding agent using OpenRouter. It can inspect a project, edit files, and run Python through workspace-scoped tools. Read-only mode, bounded runs, and saved transcripts make its behavior easier to examine.

[Explore Workbench on GitHub](https://github.com/yaqyn/workbench-ai-agent)

### CineSearch — Movie RAG Engine

![CineSearch — Movie RAG Engine](/images/projects/cinesearch-cover.png)

A movie RAG engine combining BM25 keyword scoring, semantic embeddings, chunk retrieval, hybrid ranking, reranking, and grounded generation. Evaluation tools measure retrieval quality against a golden dataset. Built while working through the Boot.dev retrieval course.

[Explore CineSearch on GitHub](https://github.com/yaqyn/cinesearch-rag-engine)

### SiteLens — Web Crawler

![SiteLens — Web Crawler](/images/projects/sitelens-cover.png)

An asynchronous website crawler with a fixed worker pool, robots.txt checks, request limits, and structured JSON reports. A practical exercise in concurrency and handling failures without losing the whole run.

[Explore SiteLens on GitHub](https://github.com/yaqyn/sitelens-web-crawler)

### Orbit — Asteroids Game

![Orbit — Asteroids Game](/images/projects/orbit-cover.png)

A Pygame arcade game. Pilot a wireframe ship, split incoming rocks, and survive with three lives. It includes pause and restart flows, a saved best score, and reduced-motion options.

[Explore Orbit on GitHub](https://github.com/yaqyn/orbit-asteroids-game)

### TextScope — Text Analyzer

![TextScope — Text Analyzer](/images/projects/textscope-cover.png)

A dependency-free text-analysis tool that counts words and letters, ranks vocabulary, compares books, and exports JSON or CSV reports.

[Explore TextScope on GitHub](https://github.com/yaqyn/textscope-text-analyzer)

### Folio — Personal Site & Generator

![Folio — Personal Site & Generator](/images/projects/folio-cover.png)

A static site generator written in Python. It turns Markdown into a linked website using a shared template and a small HTML-node model.

[Read how the site works](/notes/static-sites/) or [explore the source](https://github.com/yaqyn/folio-static-site).
