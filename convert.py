import pandas as pd
import json
import unicodedata

# Load CSV (file must be in the same folder as this script)
df = pd.read_csv("India Cities LatLng.csv")

# Build state → city → lat/lng mapping
state_city_map = {}
for _, row in df.iterrows():
    state = str(row['admin_name']).strip()
    city = str(row['city']).strip()
    lat = row['lat']
    lon = row['lng']

    # skip if state is missing
    if state == "" or state.lower() == "nan":
        continue

    # Normalize state and city names to plain ASCII
    state_ascii = unicodedata.normalize("NFKD", state).encode("ascii", "ignore").decode("ascii")
    city_ascii = unicodedata.normalize("NFKD", city).encode("ascii", "ignore").decode("ascii")

    if state_ascii not in state_city_map:
        state_city_map[state_ascii] = {}
    state_city_map[state_ascii][city_ascii] = {"lat": lat, "lon": lon}

# Save JSON in the same folder
with open("state_city_map.json", "w", encoding="utf-8") as f:
    json.dump(state_city_map, f, indent=2, ensure_ascii=True)

print("✅ state_city_map.json created successfully with ASCII-friendly names!")

