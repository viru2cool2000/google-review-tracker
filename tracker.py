response = requests.post(url, json=payload)

data = response.json()

print(data)

# Validate response
if not isinstance(data, list):
    print("Invalid API response")
    exit()

if len(data) == 0:
    print("No places found")
    exit()

place = data[0]
