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
original portrait preserves its pixels and is converted to lossless WebP
from the user’s supplied author photograph. Proportional 384/768 px lossless
derivatives let browsers choose a smaller transfer through srcset; retain the
original as the largest candidate. No forms, async controls, or loading states exist.

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
- Do not add external fonts, advertising trackers, or unnecessary JavaScript.
  Cloudflare Web Analytics is the approved deferred measurement beacon.

The biography, skills, credentials, contact details, and major-project descriptions
come from the user-maintained [GitHub profile README](https://github.com/yaqyn/yaqyn/blob/main/README.md), reviewed for this redesign. Do not invent additional personal claims.

Project branding uses three explicit categories: Career projects (HyperQuote,
Modern, Stockroom), Personal projects (qvOS, Counter), and Learning journey
projects (Little Lemon Database, Verdant Trials, Leafmark, Waymark, Readlane, Clibble, Threadline, Portlight, Workbench,
CineSearch, SiteLens, Orbit, TextScope, Folio). Keep this order on the homepage
and Projects page. The Games page follows the relative learning order, Verdant Trials,
Clibble, then Orbit. Course origins remain explicit without repeating beginner labels.

All nineteen entries appear on the homepage and Projects page. Career source
stays private. Link to approved HyperQuote and Modern showcases and the public
Yaqyn Development gallery; Stockroom remains a private evaluation prototype.
The qvOS description leads with its standalone architecture; its signed Stable
package-provider credit belongs at the end of its detailed entry. Public ISO
downloads are not claimed to be available.

The homepage remains text-led, with its original black-and-white portrait.
Detailed project entries reuse the original HyperQuote and qvOS animated covers
and the other projects' canonical artwork. Modern uses its static architectural
brand illustration. Counter and Leafmark retain their original SVG covers;
Waymark retains its lossless WebP. Little Lemon Database uses a lossless WebP
render of its approved Meta-badge cover, as requested for the project library. No organization bumper, new fonts, or
decorative effects are added to Folio. Stockroom has no public cover or
interface capture. Games keep full entries and covers on the Games page, with
short linked descriptions in the Projects inventory.

Project-cover images reserve intrinsic dimensions and load lazily. Raster
headers provide PNG/WebP geometry; canonical SVG files supply positive integer
width/height attributes. The homepage portrait remains eager and unchanged.
Asset provenance is recorded in `static/images/ASSETS.md`. Edit `content/` and
regenerate `docs/`; never maintain a second copy of page content by hand.

## Voice

Use first person selectively for introductions, ownership, and opinions. Let projects, decisions, behavior, and outcomes lead most sentences. Keep ownership clear without awkward passive wording or an invented ‘we’. Explain the purpose before the implementation. Keep paragraphs focused and headings descriptive. State course origins once where relevant, and distinguish ongoing study from completed work. Confidence comes from evidence and a point of view; humility comes from honest scope and limitations. Avoid inflated expertise, repeated beginner labels, generic enthusiasm, and claims about adoption or results without evidence.

## Publication domain

GitHub Pages serves this site at `https://yaqyn.dev/`. Production builds use the
root base path and canonical URLs on that domain. `static/CNAME` is copied into
`docs/CNAME` on every build so publishing preserves the domain. Custom base paths
remain supported for previews and other deployments.

## Search and sharing

Keep the visible lowercase wordmark and original portrait. Browser/search icons
use a self-contained off-white `y.` on charcoal, with SVG and square PNG/ICO
fallbacks. Social previews use the 1200 × 630 charcoal composition in
`static/images/social-card.webp`; preserve the portrait's proportions.

Page titles identify the owner and subject independently of the visible H1.
Canonical URLs, Open Graph/Twitter cards, and JSON-LD share the configured public
site URL. Schema describes the real person, website, page, and breadcrumbs;
never add invented ratings, credentials, publication dates, or search actions.
Generate sitemap and robots files with the site, excluding the noindex 404 page.
No fabricated last-modified dates or keyword meta tags.

The user's 2026-11-04 analytics request authorizes the existing Cloudflare Web
Analytics site's deferred beacon. Its public site token is configuration, not an
API credential. No advertising scripts or cookies are introduced by the site.
The site works without JavaScript and when analytics is blocked. The small
first-party loader only enables measurement on HTTPS production hostnames; local
previews make no analytics requests. Update its host allowlist when moving Folio. Search Console
verification and sitemap submission need the owner's authenticated Google account;
website traffic reports do not establish search impressions or indexing.

## Public profile links

The contact page prioritizes GitHub, LinkedIn, Bluesky and Contra. Patreon and
Fourthwall are support/shop destinations. YouTube, X and Gravatar remain secondary
profiles because the owner uses them less often. Telegram links to the supplied `t.me/yaqyndev` profile. Discord is the plain handle
`yaqyn`; do not fabricate a URL from a username. Meta profiles are not yet supplied.
Person structured data connects the supplied personal profiles under the aliases
`yaqyn` and `yaqyndev`; the Fourthwall shop and career organization are separate
destinations, not alternate identities of the person.

Profile links on the contact page use 16 px monochrome, locally hosted icons.
Icons are decorative CSS masks that inherit link color; labels, wrapping, focus
and keyboard targets remain readable independently. Recognizable upstream brand
assets retain their source/license notes under `static/icons/sites/`. Where no
brand vector is available, use an honest category symbol. The X label is
“X | formerly Twitter.” Browser titles remain separate from the visual wordmark.
