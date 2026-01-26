#!/usr/bin/env python3
"""
Update year archive pages with new design.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

WEB_DIR = Path(__file__).parent.parent

# New head content template
HEAD_TEMPLATE = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts from {year} - GC Mouli</title>
    <link rel="icon" type="image/png" href="favicon-32x32.png">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="styles.css">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NGJ9C40ZGL"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-NGJ9C40ZGL');
    </script>
</head>"""

HEADER_TEMPLATE = """<header>
            <h1><a href="index.html">GC Mouli</a></h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="https://sonofcauverybook.in/html/index.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>"""

FOOTER_TEMPLATE = """<footer>
            <p>&copy; 2025 Mouli Gopalakrishnan</p>
        </footer>"""


def extract_post_list(soup):
    """Extract the list of posts from the archive page."""
    main = soup.find('main')
    if not main:
        return ""

    # Find all list items
    ul = main.find('ul')
    if not ul:
        return ""

    items = []
    for li in ul.find_all('li'):
        a = li.find('a')
        if a:
            href = a.get('href', '')
            text = a.get_text().strip()
            items.append(f'                <li><a href="{href}">{text}</a></li>')

    return '\n'.join(items)


def update_archive(archive_path, year):
    """Update a single year archive page."""
    try:
        with open(archive_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        post_list = extract_post_list(soup)

        # Build new HTML
        new_html = f"""<!DOCTYPE html>
<html lang="en">
{HEAD_TEMPLATE.format(year=year)}
<body>
    <div class="container">
        {HEADER_TEMPLATE}

        <main>
            <h2>Posts from {year}</h2>
            <ul class="blog-list">
{post_list}
            </ul>
            <p style="margin-top: 2rem;"><a href="blog.html" class="year-link">&larr; Back to all posts</a></p>
        </main>

        {FOOTER_TEMPLATE}
    </div>
</body>
</html>
"""

        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        return True, None

    except Exception as e:
        return False, str(e)


def main():
    """Update all year archive pages."""
    years = range(2005, 2026)
    success = 0
    errors = []

    for year in years:
        archive_path = WEB_DIR / f"{year}.html"
        if archive_path.exists():
            ok, error = update_archive(archive_path, year)
            if ok:
                success += 1
                print(f"  Updated {year}.html")
            else:
                errors.append((f"{year}.html", error))
        else:
            print(f"  Skipped {year}.html (not found)")

    print(f"\nCompleted: {success} archive pages updated")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, error in errors:
            print(f"  - {name}: {error}")


if __name__ == '__main__':
    main()
