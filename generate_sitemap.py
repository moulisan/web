import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_sitemap(base_url, directory):
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                url = SubElement(urlset, "url")
                loc = SubElement(url, "loc")
                path = os.path.join(root, file).replace(directory, '').replace('\\', '/')
                if path.startswith('/'):
                    path = path[1:]
                if file == 'index.html':
                    path = path.replace('index.html', '')
                loc.text = f"{base_url}/{path}"
                lastmod = SubElement(url, "lastmod")
                lastmod.text = datetime.now().strftime("%Y-%m-%d")

    xml_string = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    with open("sitemap.xml", "w") as f:
        f.write(xml_string)

if __name__ == "__main__":
    base_url = "https://gcmouli.com"  # Update this to your domain
    directory = "."  # Current directory
    generate_sitemap(base_url, directory)
    print("Sitemap generated successfully.")