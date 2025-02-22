import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://www.zomato.com/bangalore/the-rameshwaram-cafe-3-indiranagar-bangalore/order"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    # Make the request
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    exit()

try:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find script tags that might contain JSON data
    script_tags = soup.find_all("script")

    # Look for JSON data (Zomato often embeds it in a script tag)
    json_data = None
    for script in script_tags:
        if script.string and "window.__INITIAL_STATE__" in script.string:
            try:
                # Extract the JSON portion
                json_str = script.string.split("window.__INITIAL_STATE__ = ")[1].split("};")[0] + "}"
                json_data = json.loads(json_str)
                break  # Assuming we found the main data block
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                continue

    if json_data is None:
        print("Failed to find JSON data in script tags.")
        exit()

    # Save or print the JSON for inspection
    try:
        with open("zomato_data.json", "w") as f:
            json.dump(json_data, f, indent=4)
        print("JSON data saved to 'zomato_data.json'")
    except IOError as e:
        print(f"Failed to write JSON data to file: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")