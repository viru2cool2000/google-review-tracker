import os

token = os.getenv("APIFY_TOKEN")

print("TOKEN EXISTS:", token is not None)

if token:
    print("FIRST 15 CHARS:", token[:15])
