#!/usr/bin/env python3
"""
Build script for dosawithmouli.html
Reads dosawithmouli-data.json, generates a static timeline page.
Run: python3 build-dosawithmouli.py
"""

import json
import os
from collections import defaultdict
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "dosawithmouli-data.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "dosawithmouli.html")

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}

# X (Twitter) icon SVG
X_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>'''

# LinkedIn icon SVG
LINKEDIN_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>'''


def format_date(date_str):
    parts = date_str.split("-")
    year = parts[0]
    month = MONTH_NAMES.get(parts[1], parts[1]) if len(parts) > 1 else ""
    return f"{month} {year}"


def build_card(entry):
    date_display = format_date(entry["date"])
    person = entry["person"]
    venue = entry["venue"]
    photo = entry.get("photo", "")
    twitter = entry.get("twitter")
    linkedin = entry.get("linkedin")

    photo_html = ""
    if photo:
        photo_html = f'''<div class="card-photo">
                <img src="{photo}" alt="Dosa with {person}" onerror="this.parentElement.classList.add('no-photo')">
            </div>'''

    social_links = []
    if twitter:
        social_links.append(
            f'<a href="{twitter}" target="_blank" rel="noopener noreferrer" aria-label="View on X" class="social-icon">{X_ICON}</a>'
        )
    if linkedin:
        social_links.append(
            f'<a href="{linkedin}" target="_blank" rel="noopener noreferrer" aria-label="View on LinkedIn" class="social-icon">{LINKEDIN_ICON}</a>'
        )
    social_html = "\n                ".join(social_links) if social_links else ""

    return f'''<div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-card">
                {photo_html}
                <div class="card-content">
                    <h3 class="card-person">{person}</h3>
                    <p class="card-date">{date_display}</p>
                    <p class="card-venue">{venue}</p>
                    <div class="card-social">
                        {social_html}
                    </div>
                </div>
            </div>
        </div>'''


def build_html(entries):
    # Sort newest first
    entries.sort(key=lambda e: e["date"], reverse=True)

    # Group by year
    by_year = defaultdict(list)
    for entry in entries:
        year = entry["date"].split("-")[0]
        by_year[year].append(entry)

    total = len(entries)

    # Build timeline sections
    timeline_html = ""
    for year in sorted(by_year.keys(), reverse=True):
        cards = "\n        ".join(build_card(e) for e in by_year[year])
        timeline_html += f'''
        <div class="year-group">
            <h2 class="year-heading">{year}</h2>
            {cards}
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#DosaWithMouli - GC Mouli</title>
    <link rel="icon" type="image/png" href="favicon-32x32.png">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NGJ9C40ZGL"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-NGJ9C40ZGL');
    </script>

    <style>
        :root {{
            --cream: #FAF8F5;
            --warm-white: #FFFEFA;
            --ink: #2C2416;
            --muted: #6B5D4D;
            --accent: #7C5E4A;
            --accent-hover: #5C4535;
            --border: #E8E2D9;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        html {{
            font-size: 18px;
        }}

        body {{
            font-family: 'Lora', Georgia, serif;
            line-height: 1.75;
            color: var(--ink);
            background-color: var(--cream);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .page-container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 0 2rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        /* Navigation */
        nav {{
            padding: 2rem 0;
            font-family: 'Source Sans 3', sans-serif;
        }}

        nav ul {{
            list-style: none;
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }}

        nav a {{
            color: var(--muted);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            transition: color 0.2s;
        }}

        nav a:hover {{
            color: var(--ink);
        }}

        nav a.active {{
            color: var(--ink);
        }}

        /* Hero */
        .hero {{
            padding: 4rem 0 2rem;
        }}

        .hero h1 {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 3.5rem;
            font-weight: 600;
            line-height: 1.1;
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
        }}

        .hero .intro {{
            font-size: 1.1rem;
            color: var(--muted);
            line-height: 1.7;
            max-width: 600px;
        }}

        /* Stats */
        .stats {{
            padding: 1.5rem 0 2.5rem;
            border-bottom: 1px solid var(--border);
            font-family: 'Source Sans 3', sans-serif;
        }}

        .stats p {{
            font-size: 0.95rem;
            color: var(--muted);
            letter-spacing: 0.05em;
        }}

        .stats strong {{
            color: var(--accent);
            font-weight: 600;
        }}

        /* Timeline */
        .timeline {{
            padding: 2rem 0 3rem;
            position: relative;
        }}

        .year-group {{
            position: relative;
            padding-left: 2.5rem;
        }}

        .year-group::before {{
            content: '';
            position: absolute;
            left: 6px;
            top: 0.5rem;
            bottom: 0;
            width: 1px;
            background: var(--border);
        }}

        .year-group:last-child::before {{
            bottom: 2rem;
        }}

        .year-heading {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--ink);
            margin-bottom: 1.5rem;
            margin-left: -2.5rem;
            padding-left: 2.5rem;
            position: relative;
        }}

        .year-heading::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: var(--accent);
        }}

        /* Timeline items */
        .timeline-item {{
            position: relative;
            margin-bottom: 2rem;
        }}

        .timeline-dot {{
            position: absolute;
            left: -2.5rem;
            top: 1.5rem;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--border);
            margin-left: 3px;
        }}

        /* Cards */
        .timeline-card {{
            background: var(--warm-white);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            transition: box-shadow 0.2s;
        }}

        .timeline-card:hover {{
            box-shadow: 0 2px 12px rgba(44, 36, 22, 0.08);
        }}

        .card-photo {{
            width: 100%;
            aspect-ratio: 3 / 2;
            overflow: hidden;
            background: var(--border);
        }}

        .card-photo img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .card-photo.no-photo {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--muted);
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.85rem;
        }}

        .card-photo.no-photo::after {{
            content: 'Photo coming soon';
        }}

        .card-photo.no-photo img {{
            display: none;
        }}

        .card-content {{
            padding: 1.25rem 1.5rem;
        }}

        .card-person {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .card-date {{
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.85rem;
            color: var(--muted);
            margin-bottom: 0.15rem;
        }}

        .card-venue {{
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.85rem;
            color: var(--muted);
        }}

        .card-social {{
            margin-top: 0.75rem;
            display: flex;
            gap: 0.75rem;
        }}

        .social-icon {{
            color: var(--muted);
            transition: color 0.2s;
        }}

        .social-icon:hover {{
            color: var(--accent);
        }}

        /* Footer */
        footer {{
            padding: 2rem 0;
            margin-top: auto;
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.8rem;
            color: var(--muted);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            html {{
                font-size: 16px;
            }}

            .page-container {{
                padding: 0 1.5rem;
            }}

            .hero {{
                padding: 3rem 0 1.5rem;
            }}

            .hero h1 {{
                font-size: 2.5rem;
            }}

            nav ul {{
                gap: 1.25rem;
            }}

            .year-heading {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="page-container">
        <nav>
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="https://sonofcauverybook.in/html/index.html">Son of Cauvery</a></li>
                <li><a href="https://www.flickr.com/photos/gcmouli/" target="_blank" rel="noopener noreferrer">Photography</a></li>
                <li><a href="dosawithmouli.html" class="active">#DosaWithMouli</a></li>
            </ul>
        </nav>

        <header class="hero">
            <h1>#DosaWithMouli</h1>
            <p class="intro">Unstructured breakfast conversations with interesting people over dosa. Started around 2017 at Sukh Sagar, Koramangala, and still going.</p>
        </header>

        <section class="stats">
            <p><strong>{total}</strong> conversations and counting</p>
        </section>

        <main class="timeline">
            {timeline_html}
        </main>

        <footer>
            <p>&copy; 2025 Mouli Gopalakrishnan</p>
        </footer>
    </div>
</body>
</html>'''


def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found")
        return

    with open(DATA_FILE, "r") as f:
        entries = json.load(f)

    html = build_html(entries)

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE} with {len(entries)} entries")


if __name__ == "__main__":
    main()
