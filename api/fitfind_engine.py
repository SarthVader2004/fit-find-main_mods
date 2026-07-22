"""
FitFind — Reasoning Engine 🧠
-------------------------------------------------
Core backend logic that:
- Loads the multimodal Fashion Knowledge Graph
- Extracts fashion concepts from text queries
- Finds relevant items & explanations
- Returns structured reasoning output
"""

import os
import pickle
import networkx as nx
from kg.explain import load_kg, explain_item, extract_concepts_from_query


# ==========================================================
# Load Knowledge Graph
# ==========================================================
def load_fitfind_kg():
    """Load FitFind's visual-aware Knowledge Graph (pickle safe)."""
    path = "./outputs/fitfind_kg_visual.pickle"
    print(f"📂 Loading Knowledge Graph from {path} ...")

    if not os.path.exists(path):
        print("❌ KG not found! Run build_kg.py first.")
        return None

    try:
        return nx.read_gpickle(path)
    except Exception:
        with open(path, "rb") as f:
            return pickle.load(f)


# Load once globally for performance
G = load_fitfind_kg()


# ==========================================================
# Generate FitFind Reasoning Response
# ==========================================================
def generate_fitfind_response(query: str):
    """
    Generates explainable recommendations for a user query.
    """
    if not G:
        return {
            "intent": "fallback",
            "response": "Knowledge Graph not loaded.",
            "explanation": "Please rebuild the KG using build_kg.py.",
        }

    print(f"\n🧩 Processing query: {query}")
    concepts = extract_concepts_from_query(query)

    if not concepts:
        print("⚠️ No recognizable fashion concepts found.")
        return {
            "intent": "fallback",
            "response": "I couldn’t detect any clear fashion concept in your query.",
            "explanation": "Fallback triggered due to low semantic confidence.",
        }

    # Pick one item node for explanation (you can enhance this later)
    item_node = next((n for n, d in G.nodes(data=True) if d.get("type") == "Item"), None)

    if not item_node:
        return {
            "intent": "fallback",
            "response": "No fashion items found in the KG.",
            "explanation": "The KG seems empty or not linked properly.",
        }

    # Generate explainability
    explanations = explain_item(G, item_node, query)

    # Combine concepts for summary
    summary_concepts = ", ".join(
        [f"{ctype.lower()} ({', '.join(vals)})" for ctype, vals in concepts.items()]
    )

    response_text = (
        f"Based on your query '{query}', I found fashion items related to {summary_concepts}. "
        f"Here’s why they match your style preferences."
    )

    return {
        "intent": "fitfind",
        "response": response_text,
        "explanation": explanations,
    }
