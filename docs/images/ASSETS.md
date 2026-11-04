# Portfolio image sources

The original black-and-white author portrait, HyperQuote/qvOS GIFs, and ten
existing learning-project covers are unchanged. The learning covers were
compared byte-for-byte with their maintained repository README artwork during
the 2026-10-18 update. Original palettes, vector markup, GIF metadata, and raster
credits are preserved.

## New project artwork

| Local file under `projects/` | Published source | SHA-256 |
| --- | --- | --- |
| `verdant-trials-cover.webp` | [Canonical cover](https://github.com/yaqyn/verdant-trials/blob/main/docs/cover.webp) | `625f03bb1696c2c2b369efc9f4ade278f9b4c6ea7af018d8537217ca633d78ae` |
| `modern-cover.webp` | [Canonical cover](https://github.com/yaqyn/Modern/blob/main/docs/readme/cover.webp) | `394fef31923693ac31b3b5dd1bd4dfcefae19c2a9c61298b1120c5ecf9338a72` |
| `counter-cover.svg` | [Canonical cover](https://github.com/yaqyn/omarchy-counter/blob/main/readme-assets/cover.svg) | `d213fab5512f304b3bb405a25aac2e74456784bfc0aad6de9e415e7b99145e01` |
| `leafmark-cover.svg` | [Canonical cover](https://github.com/yaqyn/leafmark-notebook/blob/main/readme-assets/cover.svg) | `730d9a7816f2f51abbd08c20dead29098e1477d150f14c978de58fad32b18c4a` |
| `waymark-cover.webp` | [Canonical cover](https://github.com/yaqyn/waymark-link-shortener/blob/main/readme-assets/cover.webp) | `8c4f99fc4cddc4ab8c86a2407b9251374cbd3cae45ca070c1b2001136ff4a06e` |

Modern's cover is illustrative architectural brand artwork, not a photograph of
a completed Modern project. Counter's cover documents its identity; the actual
plugin inherits the desktop theme. Leafmark and Counter remain SVGs without
rasterization. New images are exact copies of their canonical sources.

Stockroom is a private evaluation prototype. No internal data, source, screenshots,
or unpublished client material is included. The organization dust bumper stays
on the organization profile, separate from Folio's existing charcoal identity.

## Site identity and social preview

The `y.` favicon is an original vector monogram using the site's charcoal
`#1c1d20`, off-white `#f2f1ed`, and pale-gray `#deddd9` tokens. The letter is
outlined geometry, so SVG rendering does not depend on a font. It is exported
as a 48 px PNG, 180 px Apple touch icon, 192/512 px application icons, and a
16/32/48 px ICO for browser compatibility. The master is `../favicon.svg`.

`social-card.svg` is the 1200 × 630 composition source. It places the unchanged
`yaqyn-portrait.webp` file proportionally alongside the lowercase wordmark,
author name, visible areas of work, and public domain. It references that local
portrait and uses Liberation Sans with Arial/sans-serif fallbacks; the published
WebP has its typography baked in and requires no font downloads. No generated
portrait, retouching, decorative effects, or external assets are used.

The social card was rendered with `rsvg-convert`, converted through ImageMagick
to lossless WebP, and compared against the rendered PNG with zero differing
pixels. ExifTool retained only the owner's XMP Creator and Rights fields.

| File | Dimensions | SHA-256 |
| --- | --- | --- |
| `/favicon.svg` | 64 × 64 | `4dad4c8b6fa928a3b2f3794ad6d358e9b6a19320b92ff71b0fd7d6df33e0584b` |
| `/favicon.ico` | 16 / 32 / 48 px | `015b69370d6b4c68d8d2b583f6fc1c8ab4500d87bab9f2e7ce88de745bb80887` |
| `/favicon-48.png` | 48 × 48 | `45faf36f388c99e54f24e93877962ef3041f78ed2cc0d0e5b149f9ed1ba479ba` |
| `/apple-touch-icon.png` | 180 × 180 | `507e745b99d1f3814c0c576ca15ab7fe32e046189557831fee922733c9b05291` |
| `/icon-192.png` | 192 × 192 | `b6f88862cb6003c5ad8751bb3e681df1c92e9920136f6bf6d6465514c281dec7` |
| `/icon-512.png` | 512 × 512 | `baa1c177d241801c1d41b9ab1decea45238fdc9d2995d41cc3e9d1a890ff6207` |
| `/images/social-card.svg` | 1200 × 630 | `af7e4d2e5a0bc58d358d90db6e7706b303b903f83ae24557d5cd7b5c0660fce4` |
| `/images/social-card.webp` | 1200 × 630 | `10aead9f47bec1c73d351cd6eba34800fb23b2bc2d8af9f4a687882b4387417c` |

## Responsive portrait variants

`yaqyn-portrait-384.webp` (384 × 480) and `yaqyn-portrait-768.webp` (768 × 960)
are proportionally resized derivatives of the original 1122 × 1402 portrait.
ImageMagick's aspect-preserving resize rounds each output height to the nearest
whole pixel; no crop or retouching is applied. Both
derivatives use lossless WebP encoding and retain only the owner's XMP Creator
and Rights fields. The canonical portrait file remains byte-for-byte unchanged.
Use the derivatives for responsive delivery while retaining the original for
large displays and provenance.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `yaqyn-portrait-384.webp` | 121,252 | `de90bdb111ec12d85765c2c370725298be09f42e9f5ab87a3474186aabf9d618` |
| `yaqyn-portrait-768.webp` | 502,512 | `5363678b2bd1889615bd8f8ee664539bb919e75671be55af3777652e3105603c` |
