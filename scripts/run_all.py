import os
import sys

# Ensure the repository root is on sys.path so `from scripts...` imports
# work whether this file is run from the repo root or from inside the
# `scripts/` directory directly.
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Use absolute imports from the `scripts` package so imports work when
# running this file from the repository root.
from scripts.preprocess_images import process_images
from scripts.preprocess_indofashion import preprocess_indofashion
from scripts.preprocess_fashionmnist import preprocess_fashionmnist
from scripts.combine_datasets import combine_datasets


def main():
    print("🚀 Starting FitFind Phase 1 preprocessing pipeline...")

    indo = preprocess_indofashion(
        input_json_path="data/indo-fashion-dataset/train_data.json",
        images_dir="data/indo-fashion-dataset/images",
        output_path="processed/indofashion_clean.json"
    )

    fm = preprocess_fashionmnist("processed/fashionmnist_clean.json")

    combine_datasets(
        indo_path="processed/indofashion_clean.json",
        fm_path="processed/fashionmnist_clean.json",
        output_path="processed/fitfind_combined.json"
    )

    # 🧼 Image preprocessing and normalization
    process_images(
        json_path="processed/fitfind_combined.json",
        output_dir="processed_images/indofashion"
    )

    print("🎯 Phase 1 completed successfully.")


if __name__ == "__main__":
    main()
