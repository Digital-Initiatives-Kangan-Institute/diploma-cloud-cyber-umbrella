# Kangan Institute — brand reference (teaching materials)

**Purpose.** Brand spec for the *real* Kangan Institute assets we produce — chiefly the
**teaching decks**. These are delivered by Kangan and so wear Kangan/BKI branding.

> **Not to be confused with the YAT brand.** YAT College is the in-world *case study*; its
> brand (teal/terracotta/ochre — see `scenario/branding/brand-pack.md`) belongs **inside the
> scenario documents** (business cases, solution designs, the intranet). The teaching deck that
> *wraps around* the scenario is a Kangan asset and uses **this** brand. Keep the two separate.

**Provenance.** Extracted 2026-06-01 from the live `kangan.edu.au` stylesheet
(`/etc.clientlibs/bendigokangan/clientlibs/clientlib-site…css`), reading the `.kangan-theme`
CSS custom-property block — i.e. Kangan's own design tokens, not a guess. The site is a Bendigo
Kangan Institute (BKI) AEM build carrying two themes: `.kangan-theme` (gold, below) and
`.bendigo-theme` (teal, `--primary:#009390` — Bendigo TAFE's, not ours).

---

## Palette (`.kangan-theme` tokens)

| Role | Hex | Token | Use |
|---|---|---|---|
| **Primary — gold/amber** | `#EDAB0C` | `--primary` | the signature Kangan colour: accents, rules, table headers, the active marker |
| Gold dark / hover | `#D68E10` | `--primary-hover` / `--primary-dark` | depth, hover, darker fills on white |
| Gold bright | `#FBB900` | `--active-tab` | highlight / active state |
| **Secondary — charcoal** | `#2A2929` | `--secondary` | headings, dark backgrounds, body ink |
| Near-black | `#000000` | `--text` / `--black` | body text |
| Grey 1 | `#484848` | `--gray-1` | secondary text |
| Grey 2 | `#7A7A7A` | `--gray-2` / `--secondary-light` | muted text, captions |
| Border | `#CCCCCC` | `--border` | table/box outlines |
| Background light | `#F9F9F9` | `--bg-light` | takeaway/section tint |
| White | `#FFFFFF` | `--background` / `--white` | primary slide background |

**Category accents** (BKI assigns these per study area; use them to differentiate sections):

| Accent | Hex | Token |
|---|---|---|
| Magenta | `#92268F` | `--purple` |
| Sky blue | `#27B5CE` | `--skyblue` |
| Green (deep teal-green) | `#205F61` | `--green` |
| Navy | `#004488` | `--navy` |
| Red | `#C92626` | `--red` |

> Note: **magenta is an accent, not the primary** — Kangan's primary is the gold. The buttons on
> the live site use navy `#164583`/`#004488`; gold is the brand-identity colour.

## Typography

- **Roboto** family: `--font-light: robotolight`, `--font-medium: robotomedium`,
  `--font-bold: robotobold`. Headings = Roboto Bold; body = Roboto / Roboto Light.
- Deck fallback if Roboto isn't installed on a delivery machine: Calibri/Arial (close metrics).

## Logo

- Site asset referenced as `KI-TV-logos-colour…png` (full-colour institutional mark). We don't
  hold the vector. **Current decks use a typographic placeholder** — "Kangan" (charcoal) +
  "Institute" (gold) in Roboto Bold — pending the real logo file. **TBD** — obtain the official
  logo (and confirm clear-space / minimum-size rules) before any external-facing use.

## Visual style (observed)

Clean, modern, photographic; gold as the hero accent on white or charcoal; generous white space;
sans-serif throughout; tagline "Unleash You". Corporate-but-approachable TAFE positioning.

---

## Applying it to the teaching deck

**Adopted as the brand for all teaching decks (2026-06-01).** All brand + layout code lives in **`scripts/kangan_deck.py`** — the shared base for every deck. Per-Topic builders (`build_kangan_topic1_deck.py`, `build_kangan_topic2_deck.py`, `build_kangan_topic3_deck.py`, …) are **content-only**: they `import kangan_deck as k` and assemble slides from its layouts. Conventions used:

- **16:9**, white slides, charcoal text, **gold primary** for title rules, table headers,
  the active marker (`■`) and footer rule.
- **Title & close slides** = charcoal background, gold side-bar, white type.
- **Section dividers** = a full-height accent panel (one accent per section: S1 magenta /
  S2 sky / S3 green) with a large section number, on white.
- **Activity slides** = gold (or section-accent) header band + a charcoal "ACTIVITY" pill +
  a `⏱` timer chip — the activity format settled during the build.
- **Key-takeaways slides** = light-tint background, each point on a white card with an accent edge.
- **Footer** = "Kangan Institute" wordmark + page number on a thin accent rule.

> **Base module:** `scripts/kangan_deck.py` holds all brand + layout code (the same role `pptx_brand.py`
> serves for the YAT board decks). Every teaching deck imports it; per-Topic builders carry content only.
> To start a new deck: `import kangan_deck as k`, `prs = k.new_deck()`, assemble with the layouts, `k.save(prs, path)`.
