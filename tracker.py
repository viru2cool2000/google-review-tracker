import requests
import json
import os
from datetime import datetime

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

FILE_NAME = "reviews.json"

url = f"https://api.apify.com/v2/acts/compass~google-maps-extractor/run-sync-get-dataset-items?token={APIFY_TOKEN}"

payload = {
    "searchStringsArray": [
        "Chandukaka Saraf Kalaburagi"
    ],
    "maxCrawledPlacesPerSearch": 1
}

response = requests.post(url, json=payload)

data = response.json()

print(data)

place = data[0]

business_name = place.get("title", "Unknown")
current_reviews = place.get("totalScoreReviews", 0)
rating = place.get("stars", 0)

# Previous review count
old_reviews = 0

if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, "r") as file:
            saved = json.load(file)
            old_reviews = saved.get("count", 0)
    except:
        pass

new_reviews = current_reviews - old_reviews

if new_reviews < 0:
    new_reviews = 0

message = f"""
📍 {business_name}

⭐ Rating: {rating}
📝 Total Reviews: {current_reviews}
🆕 New Reviews: {new_reviews}

📅 {datetime.now().strftime('%d-%m-%Y %H:%M')}
"""

print(message)

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

# Save latest count
with open(FILE_NAME, "w") as file:
    json.dump({"count": current_reviews}, file)
