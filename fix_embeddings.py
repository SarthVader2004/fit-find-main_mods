import json
import numpy as np
import os

# Path to your final embeddings file
path = "./outputs/final_embeddings.json"

if not os.path.exists(path):
    print("❌ File not found! Make sure final_embeddings.json exists in ./outputs/")
    exit()

print("🔍 Checking and flattening nested embeddings...")

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed_count = 0

for item in data:
    for key in ["image_embedding", "text_embedding"]:
        emb = np.array(item.get(key, []))
        # Flatten nested embeddings like [[0.1, 0.2, ...]]
        if emb.ndim > 1:
            item[key] = emb.flatten().tolist()
            fixed_count += 1

# Overwrite the original file
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✅ Fixed nested embeddings successfully. ({fixed_count} items updated)")
