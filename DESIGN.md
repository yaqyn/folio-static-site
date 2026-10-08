---
version: alpha
name: yaqyn
description: A personal workshop for Abdulrahman M. Yaqyn's software, systems, and development notes.
colors:
  background: "#1c1d20"
  surface: "#27292c"
  foreground: "#f2f1ed"
  muted: "#b0b2b6"
  primary: "#deddd9"
  border: "#45474b"
typography:
  display:
    fontFamily: "Trebuchet MS, Arial, sans-serif"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, sans-serif"
  mono:
    fontFamily: "ui-monospace, Cascadia Code, DejaVu Sans Mono, monospace"
rounded:
  DEFAULT: "8px"
spacing:
  page-max: "1160px"
  section-gap: "5rem"
components:
  wordmark:
    textColor: "{colors.foreground}"
    typography: "{typography.display}"
  navigation:
    textColor: "{colors.muted}"
    typography: "{typography.body}"
  primary-link:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.background}"
    typography: "{typography.body}"
    rounded: "{rounded.DEFAULT}"
  code-block:
    backgroundColor: "{colors.surface}"
    typography: "{typography.mono}"
  divider:
    backgroundColor: "{colors.border}"
---

## Overview

A personal portfolio and notebook, grounded in the user's name and real projects.
The site's job is to introduce yaqyn and let visitors explore the work and source.
English is the current content language; no market-specific claims are made.
The register is a personal brand/content site, not a dashboard or application.

The creative reference is a graphite studio built around the user’s black and
white author portrait. The lowercase wordmark and unchanged portrait are the
signature. Charcoal backgrounds are deliberately lighter than pure black; layered
gray surfaces and off-white typography keep the photo’s contrast readable. Keep
the rest of the site calm, readable, and direct. Project descriptions explain actual behavior rather
than inventing clients, awards, career history, or availability.

Runtime CSS in `static/index.css` is canonical (mapping model B). This document
mirrors those values and records intent. This replaces the course's fantasy
identity as explicitly requested. No separate product/admin UX contract applies.

## Colors

Frontmatter maps to `--background`, `--surface`, `--foreground`, `--muted`,
`--accent`, and `--border`, respectively. Links, focus, selection, and the primary
homepage action consume `--accent`. The default is dark; forced-colors mode keeps
system-operable focus and control boundaries. Avoid adding unrelated accent hues.

## Typography

The three families map to `--font-display`, `--font-body`, and `--font-mono`.
No remote font requests or font swaps. The large lowercase homepage wordmark is
the expressive moment; article headings and body copy remain restrained.
Body line height is 1.75. Page headings scale with the viewport. Monospace is for
breadcrumbs, section labels, and code, not long prose.

## Layout

`--page-max` bounds the shared shell at 1160px. Desktop padding is 36px; it becomes
24px below 800px and 20px below 600px. The home hero is two columns on desktop,
stacked on narrow screens. Project and note links use open rows with dividers,
not elevated cards. Article text stays within 760px.

The header and footer are shared in `template.html`. Navigation wraps naturally,
without a JavaScript menu. The first keyboard target is Skip to content. Article
breadcrumbs and selected navigation retain orientation. Hero image aspect ratio
reserves space before loading at a 4:5 ratio on desktop and mobile. The
portrait file is copied unchanged from the user’s supplied author photograph. No forms, async controls, or loading states exist.

## Elevation & Depth

No shadows, gradients, glass panels, or animated backgrounds. Depth belongs to
the photographic lighting in the portrait. UI hierarchy uses type, spacing, and borders.

## Shapes

`--radius` is 8px for images, code blocks, and the primary link. The wordmark,
dividers, and open project rows retain simple geometry. Focus is always visible.

## Components

`template.html` owns the header, navigation, skip link, metadata, main landmark,
and footer. `generate_page` owns active navigation and route metadata. The home
layout uses the first three Markdown paragraphs for introduction, actions, and
portrait; maintain that order. All other pages use the shared article layout.

Links have underline/hover feedback and a 3px focus outline. The homepage primary
link uses accent fill with dark text. No control is represented by an empty hash
link. All meaningful art has alt text. Static navigation works without JavaScript.

Scrollbars have a global standards-based baseline and WebKit fallbacks, with
visible thumbs and hover feedback. Reduced-motion mode disables smooth scrolling.
The site makes no screen-reader support claims beyond its semantic HTML and
keyboard-visible navigation; test those contracts whenever the template changes.

## Do's and Don'ts

- Use yaqyn's real projects and name; keep claims verifiable.
- Update source Markdown, template, and CSS; regenerate `docs/` for publication.
- Keep links useful, focus visible, and narrow layouts free of horizontal overflow.
- Do not restore fantasy artwork or generic placeholder phone numbers.
- Do not add external fonts, trackers, or unnecessary JavaScript to this site.

The biography, skills, credentials, contact details, and major-project descriptions
come from the user-maintained [GitHub profile README](https://github.com/yaqyn/yaqyn/blob/main/README.md), reviewed for this redesign. Do not invent additional personal claims.
