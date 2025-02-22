from playwright.sync_api import sync_playwright
import json
import time

url = "https://www.zomato.com/bangalore/the-rameshwaram-cafe-3-indiranagar-bangalore/order"

def scrape_zomato_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        for attempt in range(3):
            try:
                page.goto(url, timeout=30000)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)

        page.wait_for_selector("body", timeout=10000)

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

        if not json_data:
            print("No JSON found in script tags. Extracting from DOM instead.")
            menu_items = page.query_selector_all(".sc-1hez2tp-0")  # Example class, adjust after inspection
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
                name = item.query_selector("h4")  # Adjust selectors based on actual HTML
                price = item.query_selector(".sc-17hxc2u-0")  # Example price class
                json_data["menu"][str(i + 1)] = {
                    "name": name.text_content() if name else "Unknown Item",
                    "price": float(price.text_content().replace("₹", "").strip()) if price else 0
                }

        with open("zomato_data.json", "w") as f:
            json.dump(json_data, f, indent=4)
        print("Data saved to 'zomato_data.json'")

        browser.close()

if __name__ == "__main__":
    scrape_zomato_data()