"""
FitFind: Combine visual (MobileNet) + textual (BERT) embeddings
into one unified multimodal representation for KG reasoning.
"""

import numpy as np
import json
import os
import random

def combine_embeddings():
    image_path = "./outputs/image_embeddings.npy"
    text_path = "./outputs/text_embeddings.npy"
    output_path = "./outputs/final_embeddings.json"

    # check if embeddings exist
    if not os.path.exists(image_path) or not os.path.exists(text_path):
        print("❌ Missing embedding files! Run image & text extractors first.")
        return

    print("🔗 Loading embeddings...")
    image_embs = np.load(image_path, allow_pickle=True).item()
    text_embs = np.load(text_path, allow_pickle=True).item()
    print(f"🖼️ {len(image_embs)} image embeddings loaded")
    print(f"💬 {len(text_embs)} text embeddings loaded")

    combined = []
    all_text_embs = list(text_embs.values())
    all_text_keys = list(text_embs.keys())

    if not all_text_embs:
        print("⚠️ No text embeddings found — cannot combine.")
        return

    # randomly assign text embedding to each image (since not all items have text)
    for i, (img_path, img_emb) in enumerate(image_embs.items()):
        text_idx = random.randint(0, len(all_text_embs) - 1)
        combined.append({
            "image_path": img_path,
            "image_embedding": img_emb,
            "text_desc": all_text_keys[text_idx],
            "text_embedding": all_text_embs[text_idx],
        })

    print(f"✅ Combined {len(combined)} image-text pairs")

    os.makedirs("outputs", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    print(f"💾 Saved final combined embeddings to {output_path}")

if __name__ == "__main__":
    combine_embeddings()
