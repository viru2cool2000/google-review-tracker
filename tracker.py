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

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )

    page.goto(
        MAPS_URL,
        timeout=90000,
        wait_until="domcontentloaded"
    )

    # wait manually
    page.wait_for_timeout(20000)

    text = page.locator("body").inner_text()

    print(text)

    matches = re.findall(
        r'([0-9,]+)\s+reviews',
        text,
        re.IGNORECASE
    )

    if matches:
        current_reviews = int(matches[0].replace(",", ""))
        print("Total Reviews:", current_reviews)
    else:
        print("Review count not found")

    browser.close()
