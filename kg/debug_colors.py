import pickle
import networkx as nx

def load_kg(path="./outputs/fitfind_kg_visual.pickle"):
    print(f"📂 Loading KG from {path}")
    try:
        return nx.read_gpickle(path)
    except Exception:
        with open(path, "rb") as f:
            return pickle.load(f)

if __name__ == "__main__":
    G = load_kg()
    color_nodes = [n for n in G.nodes if str(n).startswith("Color:")]
    print(f"🎨 Found {len(color_nodes)} color nodes.")
    print(sorted(color_nodes)[:50])  # Show the first 50
