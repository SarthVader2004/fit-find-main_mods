"""
FitFind — Visual-Aware Knowledge Graph Builder (v3)
---------------------------------------------------
Builds a hybrid Knowledge Graph combining:
- Symbolic fashion metadata (category, culture, color, occasion, material)
- Semantic similarity (BERT + MobileNet embeddings)
- Visual cues (dominant colors, brightness, pattern)

✅ Compatible with NetworkX 3.5+
✅ Handles mixed slashes (Windows-safe)
✅ Expands color normalization (30+ shades)
✅ Detects compound color names (e.g., "light blue" → blue)
✅ Fallback to Python pickle if gpickle fails
"""

import json
import os
import csv
import numpy as np
from tqdm import tqdm
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import pickle


# ==========================================================
# Helper Functions
# ==========================================================

def safe_str(x):
    """Convert any value to a safe lowercase string."""
    return "" if x is None else str(x).strip().lower()


def add_node_if_missing(G, node_name, ntype, **attrs):
    """Add a node if it doesn’t exist already."""
    if not G.has_node(node_name):
        G.add_node(node_name, type=ntype, **attrs)


# ==========================================================
# Symbolic Graph Builder
# ==========================================================

def build_symbolic_graph(preprocessed_data):
    """Build the symbolic KG (items, attributes, relations)."""
    G = nx.Graph()
    print("🧱 Building symbolic base graph...")

    for i, item in enumerate(tqdm(preprocessed_data, desc="Adding items")):
        item_id = str(item.get("image_path", f"item_{i}")).replace("\\", "/")
        item_node = f"Item:{item_id}"

        category = safe_str(item.get("category", "unknown"))
        color = safe_str(item.get("color", "unknown"))
        culture = safe_str(item.get("cultural_tag", "unknown"))
        material = safe_str(item.get("material", "unknown"))
        occasion = safe_str(item.get("occasion", "casual"))

        # Add item node
        G.add_node(item_node, type="Item",
                   category=category, color=color,
                   culture=culture, material=material, occasion=occasion)

        # Link symbolic attributes
        for label, value, relation in [
            ("Category", category, "has_category"),
            ("Culture", culture, "has_culture"),
            ("Occasion", occasion, "suitable_for"),
            ("Color", color, "has_color"),
            ("Material", material, "has_material"),
        ]:
            if value and value != "unknown":
                node = f"{label}:{value}"
                add_node_if_missing(G, node, label, name=value)
                G.add_edge(item_node, node, relation=relation)

    print(f"✅ Symbolic graph built: {len(G.nodes())} nodes, {len(G.edges())} edges.")
    return G


# ==========================================================
# Semantic Similarity Edges
# ==========================================================

def add_semantic_similarity(G, embeddings_path, threshold=0.85):
    """Add semantic similarity edges between items based on embeddings."""
    print("🔗 Adding semantic similarity edges...")

    with open(embeddings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    item_nodes, vectors = [], []

    for item in data:
        img_path = str(item.get("image_path", "")).replace("\\", "/")
        img_emb = np.array(item.get("image_embedding", []), dtype=np.float32)
        txt_emb = np.array(item.get("text_embedding", []), dtype=np.float32)

        if img_emb.ndim > 1:
            img_emb = img_emb.flatten()
        if txt_emb.ndim > 1:
            txt_emb = txt_emb.flatten()
        if img_emb.size == 0 and txt_emb.size == 0:
            continue

        combined_emb = np.concatenate([img_emb, txt_emb]) if img_emb.size > 0 and txt_emb.size > 0 else img_emb or txt_emb

        node_name = f"Item:{img_path}"
        if G.has_node(node_name):
            item_nodes.append(node_name)
            vectors.append(combined_emb)

    if not vectors:
        print("⚠️ No valid embeddings found for semantic links.")
        return G

    vectors = np.stack(vectors)
    sim_matrix = cosine_similarity(vectors)

    added = 0
    for i in range(len(item_nodes)):
        for j in range(i + 1, len(item_nodes)):
            sim = sim_matrix[i, j]
            if sim >= threshold:
                G.add_edge(item_nodes[i], item_nodes[j], relation="similar_to", weight=float(sim))
                added += 1

    print(f"✅ Added {added} semantic edges (threshold={threshold}).")
    return G


# ==========================================================
# Visual Feature Enrichment
# ==========================================================

def add_visual_features(G, visual_json_path):
    """Add visual nodes (color, brightness, pattern) from extracted visual features."""
    if not os.path.exists(visual_json_path):
        print(f"⚠️ Visual features file not found: {visual_json_path}")
        return G

    with open(visual_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("🎨 Adding visual-aware nodes (color, brightness, pattern)...")

    # Extended Fashion Color Map
    COLOR_MAP = {
        # Reds
        "dark red": "red", "light red": "red", "maroon": "red", "burgundy": "red",
        "crimson": "red", "scarlet": "red", "wine": "red",
        # Blues
        "navy": "blue", "sky blue": "blue", "aqua": "blue", "turquoise": "blue",
        "teal": "blue", "cyan": "blue", "baby blue": "blue",
        # Greens
        "olive": "green", "lime": "green", "mint": "green", "forest green": "green",
        "emerald": "green", "sea green": "green", "sage": "green",
        # Yellows / Oranges
        "mustard": "yellow", "gold": "yellow", "amber": "yellow", "orange": "yellow",
        "cream": "yellow", "beige": "yellow",
        # Purples / Pinks
        "lavender": "purple", "violet": "purple", "lilac": "purple", "mauve": "purple",
        "magenta": "pink", "fuchsia": "pink", "rose": "pink", "blush": "pink",
        "hot pink": "pink", "peach": "pink", "pink/purple": "pink",
        # Browns
        "tan": "brown", "camel": "brown", "chocolate": "brown", "coffee": "brown",
        "mocha": "brown", "caramel": "brown", "rust": "brown",
        # Grays
        "grey": "gray", "dark grey": "gray", "light grey": "gray",
        "silver": "gray", "ash": "gray",
        # Whites / Blacks
        "offwhite": "white", "ivory": "white", "snow": "white",
        "jet black": "black", "charcoal": "black",
        # Multicolor / Mixed
        "mixed": "multicolor", "multi": "multicolor", "rainbow": "multicolor"
    }

    attached_count = 0

    for i, item in enumerate(tqdm(data, desc="Adding visual attributes")):
        processed_path = str(item.get("processed_path", "")).replace("\\", "/")
        image_path = str(item.get("image_path", "")).replace("\\", "/")

        possible_nodes = [f"Item:{processed_path}", f"Item:{image_path}"]
        item_node = next((n for n in possible_nodes if G.has_node(n)), None)
        if not item_node:
            continue

        brightness = safe_str(item.get("brightness", "unknown"))
        pattern = safe_str(item.get("pattern", "unknown"))
        raw_colors = item.get("dominant_colors", [])
        if not isinstance(raw_colors, list):
            raw_colors = [raw_colors]

        # Normalize colors
        colors = []
        for c in raw_colors:
            if not c:
                continue
            c = safe_str(c)
            if c in COLOR_MAP:
                c = COLOR_MAP[c]
            colors.append(c)

        # Expand compound color names
        expanded_colors = []
        for color in colors:
            expanded_colors.append(color)
            for base in ["red", "blue", "green", "yellow", "pink", "purple", "black", "white", "gray", "brown"]:
                if base in color and base not in expanded_colors:
                    expanded_colors.append(base)
        colors = list(set(expanded_colors))

        # Add color nodes
        for color in colors:
            color_node = f"Color:{color}"
            add_node_if_missing(G, color_node, "Color", name=color)
            G.add_edge(item_node, color_node, relation="has_color")

        # Add brightness
        if brightness:
            bright_node = f"Brightness:{brightness}"
            add_node_if_missing(G, bright_node, "Brightness", name=brightness)
            G.add_edge(item_node, bright_node, relation="has_brightness")

        # Add pattern
        if pattern:
            pattern_node = f"Pattern:{pattern}"
            add_node_if_missing(G, pattern_node, "Pattern", name=pattern)
            G.add_edge(item_node, pattern_node, relation="has_pattern")

        attached_count += 1

    print(f"✅ Visual enrichment complete. Attached visual info for {attached_count} items.")
    print(f"📊 Total nodes: {len(G.nodes())}, edges: {len(G.edges())}")
    return G


# ==========================================================
# Save Graph
# ==========================================================

def save_graph(G, graph_path, csv_path):
    """Save KG safely as pickle + summary CSV."""
    try:
        import networkx.readwrite.gpickle as gpickle
        gpickle.write_gpickle(G, graph_path)
        print(f"💾 Saved KG → {graph_path}")
    except Exception as e:
        print(f"⚠️ gpickle error: {e} → saving via Python pickle.")
        with open(graph_path, "wb") as f:
            pickle.dump(G, f)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "type"])
        for n, d in G.nodes(data=True):
            writer.writerow([n, d.get('type')])

    print(f"📊 Summary saved. Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")


# ==========================================================
# Main
# ==========================================================

def main():
    preprocessed_path = "./outputs/combined_preprocessed.json"
    embeddings_path = "./outputs/final_embeddings.json"
    visual_path = "./outputs/visual_features.json"
    graph_path = "./outputs/fitfind_kg_visual.pickle"
    csv_path = "./outputs/fitfind_nodes_visual.csv"

    if not os.path.exists(preprocessed_path) or not os.path.exists(embeddings_path):
        print("❌ Missing preprocessing or embedding files. Run those first.")
        return

    with open(preprocessed_path, "r", encoding="utf-8") as f:
        preprocessed_data = json.load(f)

    G = build_symbolic_graph(preprocessed_data)
    G = add_semantic_similarity(G, embeddings_path, threshold=0.85)
    G = add_visual_features(G, visual_path)
    save_graph(G, graph_path, csv_path)


if __name__ == "__main__":
    main()
