#!/usr/bin/env python3
"""
Batch update blog posts with new design system.
Updates header, footer, adds Google Fonts, and fixes image paths.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

POSTS_DIR = Path(__file__).parent.parent / "posts"

# New head content template
HEAD_TEMPLATE = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" type="image/png" href="../favicon-32x32.png">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../styles.css">

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
            <h1><a href="../index.html">GC Mouli</a></h1>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../blog.html">Blog</a></li>
                    <li><a href="https://sonofcauverybook.in/html/index.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>"""

FOOTER_TEMPLATE = """<footer>
            <p>&copy; 2025 Mouli Gopalakrishnan</p>
        </footer>"""


def extract_title(soup):
    """Extract title from the HTML."""
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()

    # Fallback to h1 in main
    h1 = soup.find('main')
    if h1:
        h1_tag = h1.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
    return "GC Mouli's Blog"


def extract_main_content(soup):
    """Extract the main content, preserving images and text."""
    main = soup.find('main')
    if not main:
        # Try to find content in body
        body = soup.find('body')
        if body:
            # Look for content div or just get body content
            content = body.find('div', class_='content')
            if content:
                return str(content)
        return ""

    return main.decode_contents()


def fix_image_paths(content):
    """Fix Windows-style backslash paths to forward slashes."""
    # Fix ..\\media\\ to ../media/
    content = re.sub(r'\.\.\\media\\', '../media/', content)
    # Fix ..\media\ to ../media/
    content = re.sub(r'\.\.[\\]media[\\]', '../media/', content)
    return content


def update_post(post_path):
    """Update a single blog post with new design."""
    try:
        with open(post_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Extract title
        title = extract_title(soup)

        # Extract main content
        main_content = extract_main_content(soup)

        # Fix image paths
        main_content = fix_image_paths(main_content)

        # Build new HTML
        new_html = f"""<!DOCTYPE html>
<html lang="en">
{HEAD_TEMPLATE.format(title=title)}
<body>
    <div class="container">
        {HEADER_TEMPLATE}

        <main>
            <article>
{main_content}
            </article>
        </main>

        {FOOTER_TEMPLATE}
    </div>
</body>
</html>
"""

        # Write updated content
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        return True, None

    except Exception as e:
        return False, str(e)


def main():
    """Update all blog posts."""
    post_files = list(POSTS_DIR.glob('*.html'))
    total = len(post_files)
    success = 0
    errors = []

    print(f"Updating {total} blog posts...")

    for i, post_path in enumerate(sorted(post_files)):
        ok, error = update_post(post_path)
        if ok:
            success += 1
        else:
            errors.append((post_path.name, error))

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{total}")

    print(f"\nCompleted: {success}/{total} posts updated successfully")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, error in errors[:10]:
            print(f"  - {name}: {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")


if __name__ == '__main__':
    main()
