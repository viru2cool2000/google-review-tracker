import requests
import json
import os
from datetime import datetime

# Secrets
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FILE_NAME = "reviews.json"

# Apify URL
url = f"https://api.apify.com/v2/acts/compass~google-maps-extractor/run-sync-get-dataset-items?token={APIFY_TOKEN}"

payload = {
    "searchStringsArray": [
        "Chandukaka Saraf Kalaburagi"
    ],
    "maxCrawledPlacesPerSearch": 1
}

# Fetch data
response = requests.post(url, json=payload)

data = response.json()

print(data)

if not isinstance(data, list) or len(data) == 0:
    print("Invalid API response")
    exit()

place = data[0]

# Correct field names
business_name = place.get("title", "Unknown")
current_reviews = place.get("reviewsCount", 0)
rating = place.get("totalScore", 0)

# Load old reviews
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

# Message
message = f"""
📍 {business_name}

⭐ Rating: {rating}
📝 Total Reviews: {current_reviews}
🆕 New Reviews: {new_reviews}

📅 {datetime.now().strftime('%d-%m-%Y %H:%M')}
"""

print(message)

# Telegram API
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

telegram_response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Telegram Response:")
print(telegram_response.text)

# Save latest count
with open(FILE_NAME, "w") as file:
    json.dump({"count": current_reviews}, file)
