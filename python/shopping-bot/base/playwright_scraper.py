from playwright.sync_api import sync_playwright, Error as PlaywrightError
import json
import requests
from bs4 import BeautifulSoup

url = "https://www.zomato.com/bangalore/the-rameshwaram-cafe-3-indiranagar-bangalore/order"

def scrape_zomato_data_with_playwright():
    try:
        with sync_playwright() as p:
            # Launch browser with additional configuration
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()
            
            # Navigate with timeout and wait for load
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Wait for content (adjust selector if needed)
            page.wait_for_selector("body", timeout=10000)
            
            # Try to find JSON in script tags
            scripts = page.query_selector_all("script")
            json_data = None
            for script in scripts:
                content = script.inner_text()
                if content and "{" in content:
                    try:
                        start = content.find("{")
                        end = content.rfind("}") + 1
                        json_str = content[start:end]
                        json_data = json.loads(json_str)
                        break
                    except json.JSONDecodeError:
                        continue
            
            # Fallback to DOM scraping if no JSON
            if not json_data:
                print("No JSON found. Extracting from DOM.")
                menu_items = page.query_selector_all(".sc-1hez2tp-0")  # Adjust selector
                json_data = {
                    "restaurant": {
                        "id": "the-rameshwaram-cafe-3",
                        "name": "The Rameshwaram Cafe",
                        "subzone": "3655",
                        "available": True
                    },
                    "menu": {}
                }
                for i, item in enumerate(menu_items):
                    name = item.query_selector("h4")
                    price = item.query_selector(".sc-17hxc2u-0")
                    json_data["menu"][str(i + 1)] = {
                        "name": name.text_content() if name else "Unknown Item",
                        "price": float(price.text_content().replace("₹", "").strip()) if price else 0
                    }
            
            # Save data
            with open("zomato_data.json", "w") as f:
                json.dump(json_data, f, indent=4)
            print("Data saved to 'zomato_data.json'")
            
            browser.close()
            return True
    except PlaywrightError as e:
        print(f"Playwright error: {e}")
        return False

def scrape_with_requests_fallback():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all("script")
        json_data = None
        for script in scripts:
            if script.string and "{" in script.string:
                try:
                    start = script.string.find("{")
                    end = script.string.rfind("}") + 1
                    json_str = script.string[start:end]
                    json_data = json.loads(json_str)
                    break
                except json.JSONDecodeError:
                    continue
        
        if json_data:
            with open("zomato_data.json", "w") as f:
                json.dump(json_data, f, indent=4)
            print("Data saved via requests fallback to 'zomato_data.json'")
        else:
            print("No JSON found in requests fallback either. Manual inspection required.")
    else:
        print(f"Requests failed with status: {response.status_code}")

if __name__ == "__main__":
    if not scrape_zomato_data_with_playwright():
        print("Falling back to requests method...")
        scrape_with_requests_fallback()