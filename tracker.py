from playwright.sync_api import sync_playwright
import re

MAPS_URL = "https://www.google.com/maps/place/Chandukaka+Saraf+Pvt+Ltd+-+Kalaburagi"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    page = browser.new_page()

    page.goto(MAPS_URL, timeout=60000)

    page.wait_for_timeout(15000)

    body_text = page.locator("body").inner_text()

    print(body_text)

    match = re.search(r'([0-9,]+)\s+reviews', body_text, re.IGNORECASE)

    if match:
        current_reviews = int(match.group(1).replace(",", ""))
        print("Total Reviews:", current_reviews)
    else:
        print("Review count not found")

    browser.close()
