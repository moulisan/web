#!/usr/bin/env python3
"""
Blog Post Audit Script
Scans all blog posts for:
- Empty or minimal content
- Broken/missing image references
- Missing media files
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

POSTS_DIR = Path(__file__).parent.parent / "posts"
MEDIA_DIR = Path(__file__).parent.parent / "media"

def get_text_content(html_content):
    """Extract text content from HTML, excluding headers and footer."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove header, nav, footer
    for tag in soup.find_all(['header', 'nav', 'footer', 'script', 'style']):
        tag.decompose()

    # Get main content
    main = soup.find('main')
    if main:
        # Remove the h1 title
        h1 = main.find('h1')
        if h1:
            h1.decompose()
        return main.get_text(strip=True)
    return soup.get_text(strip=True)

def find_images(html_content):
    """Find all image references in HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            images.append(src)
    return images

def check_image_exists(img_src, post_path):
    """Check if an image file exists."""
    if img_src.startswith('http://') or img_src.startswith('https://'):
        return True  # External images - assume they exist

    # Handle relative paths
    if img_src.startswith('../media/'):
        img_path = MEDIA_DIR / img_src.replace('../media/', '')
    elif img_src.startswith('media/'):
        img_path = MEDIA_DIR.parent / img_src
    else:
        img_path = post_path.parent / img_src

    return img_path.exists()

def audit_posts():
    """Audit all blog posts."""
    results = {
        'total_posts': 0,
        'empty_posts': [],
        'minimal_content_posts': [],  # Less than 50 characters
        'posts_with_missing_images': [],
        'posts_with_broken_img_tags': [],
    }

    post_files = list(POSTS_DIR.glob('*.html'))
    results['total_posts'] = len(post_files)

    for post_path in sorted(post_files):
        try:
            with open(post_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check for empty/minimal content
            text_content = get_text_content(content)

            if len(text_content) < 10:
                results['empty_posts'].append({
                    'file': post_path.name,
                    'content_length': len(text_content),
                    'content_preview': text_content[:100] if text_content else '(empty)'
                })
            elif len(text_content) < 50:
                results['minimal_content_posts'].append({
                    'file': post_path.name,
                    'content_length': len(text_content),
                    'content_preview': text_content[:100]
                })

            # Check for images
            images = find_images(content)
            missing_images = []
            for img_src in images:
                if not check_image_exists(img_src, post_path):
                    missing_images.append(img_src)

            if missing_images:
                results['posts_with_missing_images'].append({
                    'file': post_path.name,
                    'missing_images': missing_images
                })

            # Check for broken img tags (empty src or malformed)
            soup = BeautifulSoup(content, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if not src or src.strip() == '':
                    if post_path.name not in [p['file'] for p in results['posts_with_broken_img_tags']]:
                        results['posts_with_broken_img_tags'].append({
                            'file': post_path.name,
                            'issue': 'Empty src attribute'
                        })

        except Exception as e:
            print(f"Error processing {post_path.name}: {e}")

    return results

def print_report(results):
    """Print audit report."""
    print("=" * 60)
    print("BLOG POST AUDIT REPORT")
    print("=" * 60)
    print(f"\nTotal posts scanned: {results['total_posts']}")

    print(f"\n--- Empty Posts ({len(results['empty_posts'])}) ---")
    for post in results['empty_posts']:
        print(f"  - {post['file']} ({post['content_length']} chars)")

    print(f"\n--- Minimal Content Posts ({len(results['minimal_content_posts'])}) ---")
    for post in results['minimal_content_posts']:
        print(f"  - {post['file']} ({post['content_length']} chars)")
        print(f"    Preview: {post['content_preview'][:50]}...")

    print(f"\n--- Posts with Missing Images ({len(results['posts_with_missing_images'])}) ---")
    for post in results['posts_with_missing_images']:
        print(f"  - {post['file']}")
        for img in post['missing_images']:
            print(f"      Missing: {img}")

    print(f"\n--- Posts with Broken img Tags ({len(results['posts_with_broken_img_tags'])}) ---")
    for post in results['posts_with_broken_img_tags']:
        print(f"  - {post['file']}: {post['issue']}")

    print("\n" + "=" * 60)

    # Save detailed report as JSON
    report_path = POSTS_DIR.parent / 'scripts' / 'audit_report.json'
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed report saved to: {report_path}")

if __name__ == '__main__':
    results = audit_posts()
    print_report(results)
