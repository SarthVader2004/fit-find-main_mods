import json, random, os, pandas as pd

def combine_datasets(indo_path, fm_path, output_path):
    print("📦 Combining IndoFashion and FashionMNIST...")

    with open(indo_path, "r") as f:
        indo_data = json.load(f)
    with open(fm_path, "r") as f:
        fm_data = json.load(f)

    combined = indo_data + fm_data
    random.shuffle(combined)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(combined, f, indent=4)
    pd.DataFrame(combined).to_csv(output_path.replace(".json", ".csv"), index=False)

    print(f"✅ Combined dataset saved → {output_path}")
    print(f"Total records: {len(combined)}")

if __name__ == "__main__":
    combine_datasets(
        indo_path="processed/indofashion_clean.json",
        fm_path="processed/fashionmnist_clean.json",
        output_path="processed/fitfind_combined.json"
    )
