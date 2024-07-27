import os
import datetime

def generate_sitemap(root_dir, base_url, output_file):
    urls = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                url = f"{base_url}/{relative_path.replace(os.sep, '/')}"
                urls.append(url)
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{url}</loc>\n'
        sitemap_content += f'    <lastmod>{datetime.datetime.now().date()}</lastmod>\n'
        sitemap_content += '    <changefreq>monthly</changefreq>\n'
        sitemap_content += '    <priority>0.8</priority>\n'
        sitemap_content += '  </url>\n'

    sitemap_content += '</urlset>'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(sitemap_content)

if __name__ == "__main__":
    root_dir = '.'  # Root directory of your site
    base_url = 'https://moulisan.github.io'  # Base URL of your site
    output_file = 'sitemap.xml'  # Output sitemap file
    generate_sitemap(root_dir, base_url, output_file)
