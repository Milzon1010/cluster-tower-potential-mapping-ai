import pandas as pd

# Load scraped raw OSM data
df = pd.read_csv("data/osm_bekasi_bbox_towers.csv")

print(f"📥 Loaded {len(df)} rows from raw OSM CSV")

# =======================
# 1. Filter communication towers only
# =======================
df = df[df['type'].str.contains("communication", case=False, na=False)].copy()
print(f"✅ Retained {len(df)} communication towers")

# =======================
# 2. Create region label (static for now)
# =======================
df["region"] = "Bekasi"

# =======================
# 3. Extract source tag presence
# =======================
df["source_tagged"] = df["source"].apply(lambda x: bool(x and isinstance(x, str) and len(x.strip()) > 0))
df["is_hot_source"] = df["source"].str.contains("HOT", na=False)

# =======================
# 4. Optional: Generate clean ID
# =======================
df["tower_code"] = ["TW%05d" % i for i in range(1, len(df)+1)]

# =======================
# 5. Save to cleaned CSV
# =======================
df.to_csv("data/osm_cleaned_towers.csv", index=False)
print("💾 Saved cleaned data to: data/osm_cleaned_towers.csv")
