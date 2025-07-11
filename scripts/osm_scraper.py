import overpy
import folium
import pandas as pd

# Init Overpass API
api = overpy.Overpass()

# Area target (misalnya Bekasi - bisa diganti)
query = """
area["name"="Kabupaten Bekasi"]["admin_level"="6"]->.a;
(
  node["man_made"="communications_tower"](area.a);
  node["tower:type"="communication"](area.a);
  node["man_made"="tower"](area.a);
);
out center;
"""


# Run query
print("Querying Overpass API...")
result = api.query(query)

# Parse towers
tower_data = []
for node in result.nodes:
    tower_data.append({
        "id": node.id,
        "lat": node.lat,
        "lon": node.lon,
        "tags": node.tags.get("tower:type", "unknown")
    })

# Save to CSV
df = pd.DataFrame(tower_data)
df.to_csv("data/osm_bekasi_towers.csv", index=False)
print(f"✅ Saved {len(df)} towers to data/osm_bekasi_towers.csv")

# Save interactive map
m = folium.Map(location=[-6.25, 107], zoom_start=11)
for _, row in df.iterrows():
    folium.Marker([row["lat"], row["lon"]], tooltip=row["tags"]).add_to(m)

m.save("visuals/osm_tower_map.html")
print("📍 Map saved to visuals/osm_tower_map.html")
