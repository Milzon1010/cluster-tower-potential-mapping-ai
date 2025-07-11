import overpy
import folium
import pandas as pd

# ==============================
# 📍 Define Bounding Box (Bekasi area)
# Format: (south, west, north, east)
bbox = (-6.4, 106.9, -6.1, 107.2)  # kira-kira Kab. Bekasi
# ==============================

# Initialize Overpass API
api = overpy.Overpass()

# Construct query with multiple tags
query = f"""
(
  node["man_made"="tower"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["man_made"="communications_tower"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["tower:type"="communication"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""

print("⏳ Querying Overpass API...")
try:
    result = api.query(query)
except Exception as e:
    print("❌ Failed to fetch data:", e)
    exit()

print(f"🔍 Found {len(result.nodes)} tower nodes.")

# Parse nodes
tower_data = []
for node in result.nodes:
    tower_data.append({
        "id": node.id,
        "lat": node.lat,
        "lon": node.lon,
        "type": node.tags.get("tower:type", node.tags.get("man_made", "unknown")),
        "source": node.tags.get("source", ""),
    })

# Save to CSV
df = pd.DataFrame(tower_data)
df.to_csv("data/osm_bekasi_bbox_towers.csv", index=False)
print(f"✅ Saved CSV: data/osm_bekasi_bbox_towers.csv")

# Generate folium map
map_center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
m = folium.Map(location=map_center, zoom_start=11)

for _, row in df.iterrows():
    tooltip = f"{row['type']} (id: {row['id']})"
    folium.Marker([row["lat"], row["lon"]], tooltip=tooltip).add_to(m)

m.save("visuals/osm_tower_map_bbox.html")
print("📍 Map saved to visuals/osm_tower_map_bbox.html")
