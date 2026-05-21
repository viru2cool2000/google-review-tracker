from playwright.sync_api import sync_playwright
import re
import json
import os
import requests
from datetime import datetime

MAPS_URL = "https://www.google.com/maps/place/Chandukaka+Saraf+Pvt+Ltd+-+Kalaburagi/@17.3322703,76.8357625,17z/data=!3m1!4b1!4m6!3m5!1s0x3bc8c79384cd41eb:0x56fd46e579715ee7!8m2!3d17.3322703!4d76.8357625!16s%2Fg%2F11n4k0ldq8?entry=ttu&g_ep=EgoyMDI2MDUxNy4wIKXMDSoASAFQAw%3D%3D"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(MAPS_URL, timeout=60000)

page.wait_for_timeout(20000)

content = page.content()

browser.close()

print(content)

match = re.search(r'"reviews":[^0-9]*([0-9,]+)', content)

if not match:
    match = re.search(r'([0-9,]+)\sreviews', content, re.IGNORECASE)
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
