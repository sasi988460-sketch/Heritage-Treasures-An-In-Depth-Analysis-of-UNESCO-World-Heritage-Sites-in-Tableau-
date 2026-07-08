import pandas as pd
import random

random.seed(42)
countries_regions = {
    "Italy": "Europe and North America",
    "China": "Asia and the Pacific",
    "France": "Europe and North America",
    "Germany": "Europe and North America",
    "India": "Asia and the Pacific",
    "Mexico": "Latin America and the Caribbean",
    "Spain": "Europe and North America",
    "Iran": "Arab States",
    "Egypt": "Arab States",
    "Brazil": "Latin America and the Caribbean",
    "United States": "Europe and North America",
    "Japan": "Asia and the Pacific",
    "Peru": "Latin America and the Caribbean",
    "South Africa": "Africa",
    "Kenya": "Africa",
}
rows = []
for country, region in countries_regions.items():
    num_sites = random.randint(5, 25)
    for i in range(num_sites):
        year = random.randint(1978, 2019)
        danger = random.choices(["Yes", "No"], weights=[0.08, 0.92])[0]
        rows.append({
            "Name_en": f"{country} Heritage Site {i + 1}",
            "Country": country,
            "Region": region,
            "Date_inscribed": year,
            "Danger": danger,
        })
df = pd.DataFrame(rows)
import os
os.makedirs("data", exist_ok=True)
df.to_csv("data/heritage_sites.csv", index=False)
print(f"Sample dataset created: data/heritage_sites.csv ({len(df)} rows)")
