from playwright.sync_api import sync_playwright
import re
import json
import os
import requests
from datetime import datetime

MAPS_URL = "https://www.google.com/maps/search/Chandukaka+Saraf+Kalaburagi"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(MAPS_URL, timeout=60000)

    page.wait_for_timeout(10000)

    content = page.content()

    browser.close()

match = re.search(r'([0-9,]+)\sreviews', content)

if match:
    current_reviews = int(match.group(1).replace(",", ""))
else:
    current_reviews = 0

FILE_NAME = "reviews.json"

try:
    with open(FILE_NAME, "r") as file:
        data = json.load(file)
        old_reviews = data.get("count", 0)
except:
    old_reviews = 0

today_reviews = current_reviews - old_reviews

message = f"""
📍 Chandukaka Saraf – Kalaburagi

⭐ Total Reviews: {current_reviews}
🆕 Reviews Today: {today_reviews}

📅 {datetime.now().strftime('%d-%m-%Y')}
"""

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

response = requests.post(
    telegram_url,
    data={
        "chat_id": chat_id,
        "text": message
    }
)

print(message)
print(response.text)

with open(FILE_NAME, "w") as file:
    json.dump({"count": current_reviews}, file)
