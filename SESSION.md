# gcmouli.com — Session Handoff Doc
Last updated: Feb 22 2026. Written so a new Claude session can pick up exactly where we left off.

---

## Site Overview

Personal website for Mouli Gopalakrishnan (gcmouli.com). Static HTML/CSS, no build step. Deployed via GitHub Pages or similar. Google Analytics: `G-NGJ9C40ZGL`.

### File Structure
```
web/
  index.html            — homepage
  blog.html             — blog listing
  dosawithmouli.html    — #DosaWithMouli breakfast conversations page
  sideprojects.html     — side projects page (NEW)
  project-thumbs/       — thumbnail images for side projects (NEW)
    sabha.png           — Sabha OG image, copied from ~/code/Sabha/og-image.png
  dosa-photos/          — photos for DosaWithMouli cards
  build-dosawithmouli.py — script to generate dosawithmouli.html from data
  dwm-updater.py        — updater script (untracked, WIP)
  SESSION.md            — this file
```

### Design System
- Fonts: Playfair Display (headings), Lora (body), Source Sans 3 (UI/meta)
- Colors: `--cream: #FAF8F5`, `--warm-white: #FFFEFA`, `--ink: #2C2416`, `--muted: #6B5D4D`, `--accent: #7C5E4A`, `--border: #E8E2D9`
- Max-width: 720px on index/blog/sideprojects, 960px on dosawithmouli

---

## Nav Structure (all pages)

Home / Blog / Son of Cauvery / Side Projects / #DosaWithMouli

- Photography was removed from nav and interests links (Feb 22 2026)
- Side Projects added before Photography, then Photography removed
- blog.html nav was previously incomplete — now has all links

---

## Pages

### index.html
- Hero: name + "People, Product, Technology" tagline + Twitter/LinkedIn icons
- Pull quote
- About section: 5 paragraphs — (1) professional intro [unchanged], (2) Blog, (3) Son of Cauvery + ISB teaching, (4) Side Projects / vibe coding, (5) #DosaWithMouli
- Interests-links row: Blog / Son of Cauvery / Side Projects / #DosaWithMouli
- Last paragraph links to dosawithmouli.html directly (not LinkedIn search)

### blog.html
- Nav updated to match full nav structure

### dosawithmouli.html
- WIP banner below hero intro paragraph, above conversation cards
- Banner text: "WORK IN PROGRESS. PLEASE CHECK BACK LATER."
- Stats section ("10 conversations and counting") commented out
- Cards organized by year: 2025, 2024, 2023, 2022

### sideprojects.html (NEW)
- Hero: "Side Projects" + one-line intro
- Project cards: full-bleed thumbnail at top, name + link + 2-sentence description + meta
- Sabha card: thumbnail from project-thumbs/sabha.png, links to sabha-ai.vercel.app
- Meta format: "Vibe coded · Mon YYYY"
- To add a new project: copy the `.project-card` div block, drop a thumbnail in project-thumbs/

---

## Sabha (side project)

- **What it is**: AI debate entertainment app. Language models battle over spicy topics across 3 heat levels: Sane, Heated, Screamer.
- **Live at**: sabha-ai.vercel.app
- **Repo**: moulisan/Sabha (gcmouli@gmail.com account), local at ~/code/Sabha
- **Thumbnail**: ~/code/Sabha/og-image.png → copied to project-thumbs/sabha.png

---

## Session History

### Feb 22 2026
- Added sideprojects.html (new page) with Sabha as first project
- Added "Side Projects" to nav on all pages (before Photography)
- Removed Photography from nav and interests-links on all pages
- Added WIP banner to dosawithmouli.html (below hero, above cards)
- Commented out stats section on dosawithmouli.html
- Rewrote index.html about section: 5 paragraphs, one per nav item
- Changed #DosaWithMouli paragraph to link to dosawithmouli.html instead of LinkedIn search
- Created project-thumbs/ directory; Sabha OG image copied in as sabha.png
