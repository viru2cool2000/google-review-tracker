from playwright.sync_api import sync_playwright
import re
import json
import os
import requests
from datetime import datetime

MAPS_URL = "https://www.google.com/maps/place/Chandukaka+Saraf+Pvt+Ltd+-+Kalaburagi/@17.3322703,76.8357625,17z/data=!3m1!4b1!4m6!3m5!1s0x3bc8c79384cd41eb:0x56fd46e579715ee7!8m2!3d17.3322703!4d76.8357625!16s%2Fg%2F11n4k0ldq8?entry=ttu"

FILE_NAME = "reviews.json"

current_reviews = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(MAPS_URL, timeout=60000)

    # Wait for page to fully load
    page.wait_for_timeout(15000)

    content = page.content()

    browser.close()

# Try extracting reviews count
match = re.search(r'([0-9,]+)\sreviews', content, re.IGNORECASE)

if match:
    current_reviews = int(match.group(1).replace(",", ""))
else:
    print("Review count not found")
    current_reviews = 0

# Load previous review count
old_reviews = 0

if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            old_reviews = data.get("count", 0)
    except Exception as e:
        print("Error reading JSON:", e)

# Calculate new reviews
new_reviews = current_reviews - old_reviews

if new_reviews < 0:
    new_reviews = 0

message = f"""
📍 Chandukaka Saraf – Kalaburagi

⭐ Total Reviews: {current_reviews}
🆕 New Reviews: {new_reviews}

📅 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
"""

# Telegram credentials
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# Send Telegram message
try:
    response = requests.post(
        telegram_url,
        data={
            "chat_id": chat_id,
            "text": message
        }
    )

    print("Telegram Response:", response.text)

except Exception as e:
    print("Telegram Error:", e)

# Print message
print(message)

# Save latest review count
with open(FILE_NAME, "w") as file:
    json.dump({"count": current_reviews}, file)
