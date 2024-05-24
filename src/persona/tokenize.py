import requests

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully as {filename}")
    else:
        print("Failed to download PDF")

# Usage:
url = "https://github.com/slabstech/slabstech.github.io/blob/main/assets/pdf/onwards.pdf"
filename = "onwards.pdf"
download_pdf(url, filename)
