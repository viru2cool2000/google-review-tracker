import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("BOT TOKEN:", BOT_TOKEN)
print("CHAT ID:", CHAT_ID)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": "Test message from GitHub Actions"
    }
)

print(response.text)
