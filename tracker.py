from playwright.sync_api import sync_playwright
import re

MAPS_URL = "YOUR_GOOGLE_MAPS_LINK"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(MAPS_URL, timeout=60000)

    # Wait for Google Maps to load
    page.wait_for_timeout(10000)

    # Get page text
    body_text = page.locator("body").inner_text()

    print(body_text)

    # Find reviews count
    match = re.search(r'([0-9,]+)\s+reviews', body_text, re.IGNORECASE)

    if match:
        current_reviews = int(match.group(1).replace(",", ""))
        print("Reviews:", current_reviews)
    else:
        print("Review count not found")

    browser.close()
