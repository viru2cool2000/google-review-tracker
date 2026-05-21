import os

print("TOKEN EXISTS:", os.getenv("APIFY_TOKEN") is not None)
print("TOKEN:", os.getenv("APIFY_TOKEN"))
