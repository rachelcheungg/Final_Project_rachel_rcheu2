import json
import requests
from pathlib import Path

url = "https://gisportal.champaignil.gov/ms/rest/services/Open_Data/Open_Data/MapServer/8/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "geojson"
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

output_path = Path(__file__).resolve().parent.parent / "apartments" / "data"
output_path.mkdir(parents=True, exist_ok=True)

with open(output_path / "champaign_apartments.json", "w") as f:
    json.dump(data, f)

print("Saved apartments data")