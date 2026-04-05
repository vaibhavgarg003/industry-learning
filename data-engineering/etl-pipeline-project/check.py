import json

with open('data/raw_countries.json') as f:
    data = json.load(f)

print(f"Total countries: {len(data)}")
print(f"First country: {data[0]['name']['common']}")
print(f"Sample keys: {list(data[0].keys())[:5]}")