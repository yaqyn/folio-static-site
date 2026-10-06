---
description: How yaqyn's Python static site generator turns Markdown into pages, with a shared template and verified builds.
---
# Building a site from first principles

This site is a small Python program before it is a website. The content lives in Markdown files, and the generator turns those files into ordinary HTML.

## A page is a tree

Inline text becomes a set of typed nodes: text, bold, italics, links, images, and code. Blocks provide the structure around them: paragraphs, headings, lists, quotes, and fenced code.

Those pieces form a tree of parent and leaf nodes. Rendering the tree produces HTML without a framework or a browser running on the server.

```
Markdown → text nodes → HTML nodes → template → static page
```

## The small boundaries matter

Text and attributes need HTML escaping. Links need a supported scheme. A project hosted below a path such as `/my-site/` needs that prefix applied to local routes without changing external links.

The generator also builds in a temporary directory. A malformed page should fail the build while leaving the last generated site intact.

## Content stays separate

The shared template owns the navigation, metadata, and footer. Markdown owns the page. A small frontmatter block supplies a description and, for the homepage, its layout.

```
description: A short description of the page.
layout: home
```

## Try it

The launcher builds a local version and serves it on the loopback interface:

```
./launch
```

[View the source](https://github.com/yaqyn/my-site) or [return to the notes](/notes/).
