import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Define paths
export_file = 'gcmoulicom.WordPress.2024-07-05.xml'  # Replace with the path to your XML export file
output_path = './'
posts_path = os.path.join(output_path, 'posts')
media_path = os.path.join(output_path, 'media')

# Create output directories if they don't exist
os.makedirs(output_path, exist_ok=True)
os.makedirs(posts_path, exist_ok=True)
os.makedirs(media_path, exist_ok=True)

def parse_export_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return None

def clean_filename(title, existing_filenames):
    # Convert to lowercase
    filename = title.lower()
    # Replace spaces with hyphens
    filename = re.sub(r'\s+', '-', filename)
    # Remove special characters
    filename = re.sub(r'[^\w\-]', '', filename)
    # Ensure filename ends with .html
    if not filename.endswith('.html'):
        filename += '.html'
    # Ensure the filename is unique
    original_filename = filename
    counter = 1
    while filename in existing_filenames:
        filename = f"{original_filename[:-5]}-{counter}.html"
        counter += 1
    existing_filenames.add(filename)
    return filename

def create_html_file(title, body_content, filename):
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1><a href="../index.html">GC Mouli's Blog</a></h1>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../blog.html">Blog</a></li>
                    <li><a href="../sonofcauvery.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>{title}</h1>
            {body_content}
        </main>
        <footer>
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""
    with open(os.path.join(posts_path, filename), 'w', encoding='utf-8') as f:
        f.write(html_template.strip())

def process_posts(root):
    if root is None:
        print("No XML root found. Exiting.")
        return

    posts_by_date = {}
    existing_filenames = set()
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else 'Untitled'
        content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
        content = content.text if content is not None else None
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else None

        if content is None or pub_date is None:
            print(f"Skipping post '{title}' because it has no content or publication date.")
            continue

        print(f"Processing post: {title}")

        # Format publication date
        pub_date_parsed = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
        year_month = pub_date_parsed.strftime('%Y-%m')
        year = pub_date_parsed.strftime('%Y')
        date_str = pub_date_parsed.strftime('%d %b %Y')

        if year not in posts_by_date:
            posts_by_date[year] = []

        # Use BeautifulSoup to prettify the content
        soup = BeautifulSoup(content, 'html.parser')
        body_content = soup.prettify()

        # Create clean filename
        filename = clean_filename(title, existing_filenames)
        create_html_file(title, body_content, filename)

        # Add post to the list for the month and year
        posts_by_date[year].append((pub_date_parsed, date_str, title, filename))

    # Sort posts in reverse chronological order
    for year in posts_by_date:
        posts_by_date[year].sort(reverse=True, key=lambda x: x[0])

    return posts_by_date

def generate_year_page(year, posts):
    year_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts from {year}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1><a href="index.html">GC Mouli's Blog</a></h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="sonofcauvery.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Posts from {year}</h2>
            <ul>
"""
    for _, date_str, title, filename in posts:
        year_content += f'                <li><a href="posts/{filename}">{date_str} - {title}</a></li>\n'

    year_content += """
            </ul>
        </main>
        <footer>
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""

    with open(os.path.join(output_path, f'{year}.html'), 'w', encoding='utf-8') as f:
        f.write(year_content.strip())

def generate_blog_page(posts_by_date):
    blog_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>GC Mouli's Blog</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="sonofcauvery.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <div class="content">
                <section>
"""
    years = sorted(posts_by_date.keys(), reverse=True)

    for year in years:
        blog_content += f'                    <h2>{year}</h2>\n                    <ul>\n'
        for _, date_str, title, filename in posts_by_date[year][:5]:  # Display top 5 posts of the year on blog page
            blog_content += f'                        <li><a href="posts/{filename}">{date_str} - {title}</a></li>\n'
        blog_content += f'                    </ul>\n                    <a href="{year}.html">See all posts from {year}</a>\n'
    
    blog_content += """
                </section>
                <aside>
                    <h3>Archives</h3>
                    <ul>
"""
    for year in years:
        blog_content += f'                        <li><a href="{year}.html">{year}</a></li>\n'

    blog_content += """
                    </ul>
                </aside>
            </div>
        </main>
        <footer>
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""
    with open(os.path.join(output_path, 'blog.html'), 'w', encoding='utf-8') as f:
        f.write(blog_content.strip())

    # Generate yearly pages
    for year, posts in posts_by_date.items():
        generate_year_page(year, posts)

def generate_index_page():
    index_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GC Mouli</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>GC Mouli's Blog</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="sonofcauvery.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>About Me</h2>
            <p>Hello! I'm GC Mouli. I work in the tech industry and have a passion for writing and sharing knowledge.</p>
            <p>You can find me on Twitter and LinkedIn:</p>
            <ul>
                <li><a href="https://twitter.com/your_twitter_handle">Twitter</a></li>
                <li><a href="https://linkedin.com/in/your_linkedin_handle">LinkedIn</a></li>
            </ul>
        </main>
        <footer>
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""
    with open(os.path.join(output_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content.strip())

def generate_son_of_cauvery_page():
    sonofcauvery_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son of Cauvery</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>GC Mouli's Blog</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="sonofcauvery.html">Son of Cauvery</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Son of Cauvery</h2>
            <p>I am working on an English retelling of the Tamil epic novel Ponniyin Selvan, titled "Son of Cauvery".</p>
            <p>The story follows the early life of Arulmozhivarman, who later becomes the great Chola emperor Rajaraja Chola I.</p>
        </main>
        <footer>
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""
    with open(os.path.join(output_path, 'sonofcauvery.html'), 'w', encoding='utf-8') as f:
        f.write(sonofcauvery_content.strip())

if __name__ == "__main__":
    root = parse_export_file(export_file)
    posts_by_date = process_posts(root)
    generate_blog_page(posts_by_date)
    generate_index_page()
    generate_son_of_cauvery_page()
    print("Static HTML site generated successfully.")

