"""
FitFind — Visual-Aware Explainability Engine (v3) 🧠
----------------------------------------------------
Generates human-readable explanations for why a fashion item
matches a user query using a hybrid Knowledge Graph (symbolic + semantic + visual).

✅ Compatible with NetworkX 3.5+
✅ Works with visual-aware KG (`fitfind_kg_visual.pickle`)
✅ Supports color normalization (e.g., "grey" → "gray", "multi-color" → "multicolor")
✅ Handles both symbolic and visual reasoning gracefully
"""

import networkx as nx
import pickle
import os
import re


# ==========================================================
# 1️⃣ Load Knowledge Graph
# ==========================================================

def load_kg(path="./outputs/fitfind_kg_visual.pickle"):
    """
    Loads the Knowledge Graph (symbolic + semantic + visual layers).
    Handles both NetworkX gpickle and Python pickle fallbacks.
    """
    print(f"📂 Loading Knowledge Graph from {path} ...")

    if not os.path.exists(path):
        print("❌ KG file not found. Please ensure it exists in './outputs'.")
        return None

    try:
        G = nx.read_gpickle(path)
        print("✅ Loaded KG successfully using NetworkX read_gpickle().")
        return G
    except Exception as e:
        print(f"⚠️ gpickle load failed ({e}). Attempting Python pickle fallback...")
        with open(path, "rb") as f:
            G = pickle.load(f)
            print("✅ Loaded KG successfully using Python pickle fallback.")
            return G


# ==========================================================
# 2️⃣ Query Concept Extraction (Symbolic + Visual)
# ==========================================================

CATEGORIES = [
    "saree", "kurta", "lehenga", "dress", "shirt",
    "tshirt", "jeans", "jacket", "blouse", "skirt", "top", "boot"
]

OCCASIONS = [
    "wedding", "party", "office", "casual", "festival", "ethnic", "formal"
]

COLORS = [
    "red", "blue", "white", "pink", "black", "yellow",
    "green", "brown", "golden", "purple", "gray", "multicolor"
]

CULTURES = ["indian", "western", "fusion", "ethnic"]

PATTERNS = [
    "plain", "floral", "striped", "geometric", "polka",
    "textured", "complex", "patterned"
]

BRIGHTNESS = ["bright", "dark", "pastel", "dim", "light"]


def extract_concepts_from_query(query):
    """
    Extracts symbolic + visual fashion concepts from a natural language query.
    e.g. "bright pastel saree for wedding" →
    {'Category': ['saree'], 'Color': ['pastel'], 'Brightness': ['bright'], 'Occasion': ['wedding']}
    """

    # Normalize text for better matching
    query = (
        query.lower()
        .replace("grey", "gray")
        .replace("multi color", "multicolor")
        .replace("multi-color", "multicolor")
        .replace("ankleboot", "ankle boot")
    )

    concepts = {}
    concept_groups = [
        (CATEGORIES, "Category"),
        (OCCASIONS, "Occasion"),
        (COLORS, "Color"),
        (CULTURES, "Culture"),
        (PATTERNS, "Pattern"),
        (BRIGHTNESS, "Brightness"),
    ]

    for words, label in concept_groups:
        for w in words:
            if re.search(rf"\b{w}\b", query):
                concepts.setdefault(label, []).append(w)

    return concepts


# ==========================================================
# 3️⃣ Item Node Finder
# ==========================================================

def find_item_node(G, processed_path):
    """Find the corresponding Item node in the KG by image or processed path."""
    if not processed_path:
        return None
    processed_path = processed_path.replace("\\", "/")
    for n, d in G.nodes(data=True):
        if d.get("type") == "Item" and (
            d.get("processed_path") == processed_path or d.get("image_path") == processed_path
        ):
            return n
    return None


# ==========================================================
# 4️⃣ Explainability Engine
# ==========================================================

def explain_item(G, item_node, query):
    """
    Given a fashion query (e.g., "bright red saree for wedding"),
    returns explainable reasoning chains using KG relationships.
    """
    if not G or not item_node or not G.has_node(item_node):
        return [f"⚠️ Item node not found in KG: {item_node}"]

    concepts = extract_concepts_from_query(query)
    explanations = []

    for ctype, vals in concepts.items():
        for val in vals:
            node_name = f"{ctype}:{val}"
            if G.has_node(node_name):
                try:
                    path = nx.shortest_path(G, item_node, node_name)
                    path_str = " → ".join([p.split(":")[-1] for p in path])
                    emoji = "🎨" if ctype in ["Color", "Pattern", "Brightness"] else "💬"
                    explanations.append(f"{emoji} Matches '{val}' ({ctype}) — path: {path_str}")
                except nx.NetworkXNoPath:
                    continue
            else:
                explanations.append(f"⚪ No node found for {ctype.lower()} '{val}' in KG.")

    if not explanations:
        d = G.nodes[item_node]
        attrs = [f"{k}={v}" for k, v in d.items() if v and k not in ("type",)]
        if attrs:
            return [f"🧵 Item attributes: {', '.join(attrs)}"]
        else:
            return ["No explainable attributes found for this item."]

    return explanations


# ==========================================================
# 5️⃣ Interactive Command-Line Entry Point
# ==========================================================

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="Explain why a fashion item matches a user query (visual + symbolic reasoning)."
    )
    p.add_argument("--item", type=str, help="Path of image to explain (optional)")
    p.add_argument(
        "--kg",
        type=str,
        default="./outputs/fitfind_kg_visual.pickle",
        help="Path to visual-aware Knowledge Graph file",
    )
    args = p.parse_args()

    # 💬 Ask user for query interactively
    query = input("💬 Enter your fashion query: ")

    # 📂 Load the Knowledge Graph
    G = load_kg(args.kg)
    if G is None:
        print("❌ Could not load KG.")
        exit()

    # 🎯 Pick a sample item node if not provided
    if args.item:
        node = find_item_node(G, args.item)
    else:
        node = next((n for n, d in G.nodes(data=True) if d.get("type") == "Item"), None)

    print(f"\n🧩 Explaining for query: {query}")
    print(f"🎯 Item Node: {node}\n")

    explanations = explain_item(G, node, query)

    print("🪄 Explanation Results:")
    print("-" * 60)
    for e in explanations:
        print(e)
    print("-" * 60)
