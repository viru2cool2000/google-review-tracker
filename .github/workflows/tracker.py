import requests
import re
import json
import os
from datetime import datetime

URL = "https://www.google.com/maps/place/Chandukaka+Saraf+Kalaburagi"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

match = re.search(r'([0-9,]+) reviews', response.text)

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

requests.post(telegram_url, data={
    "chat_id": chat_id,
    "text": message
})

with open(FILE_NAME, "w") as file:
    json.dump({"count": current_reviews}, file)

print(message)
