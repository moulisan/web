import os
from bs4 import BeautifulSoup

def add_google_analytics(directory, tracking_id):
    tracking_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{tracking_id}');
    </script>
    """
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                
                head = soup.find('head')
                if head:
                    # Check if the tracking code is already present
                    if not head.find('script', src=f"https://www.googletagmanager.com/gtag/js?id={tracking_id}"):
                        # Append the tracking code to the head tag
                        head.append(BeautifulSoup(tracking_code, 'html.parser'))
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"Added Google Analytics to {file_path}")
                else:
                    print(f"No <head> tag found in {file_path}")

if __name__ == "__main__":
    directory = '.'  # Change this to the root directory of your HTML files
    tracking_id = 'G-NGJ9C40ZGL'  # Replace with your actual tracking ID
    add_google_analytics(directory, tracking_id)
